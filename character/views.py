import time
import logging
import json

from api.imageGenAPI import ImageGenAPI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from common.aws import AWSManager
from .models import Submit, Answer
from question.models import Question, Poll
from accounts.models import User
from .serializer import (
    SubmitSerializer,
    SubmitDetailSerializer,
    SubmitCreateSerializer,
    AnswerSerializer,
    AnswerPostSerializer,
)
from question.serializer import QuestionTextSerializer, QuestionIdSerializer

from drf_yasg.utils import swagger_auto_schema
from .swagger_serializer import (
    GetCharacterListResponseSerializer,
    GetCharacterListRequestSerializer,
    GetCharacterDetailResponseSerializer,
    PostCharacterRequestSerializer,
    PostCharacterResponseSerializer,
    GetKeywordChartResponseSerializer,
    GetURLsResponseSerializer,
    # GetCharacterInfoResponseSerializer,
    PostFinalSubmitRequestSerializer,
    PostFinalSubmitResponseSerializer,
)

from celery_worker.tasks import create_character
from celery.result import AsyncResult
from api.api import upload_img_to_s3

from common.auth import encrypt_resource_id, decrypt_resource_id

fixed_question_num = 6

# 로거 생성
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 로그를 파일로 저장하려면 다음과 같이 핸들러를 설정합니다.
file_handler = logging.FileHandler("debug.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

comprehend = AWSManager.get_comprehend_client()


def extract_key_phrases(text, min_score=0.9):
    with open("word_replacements.json", "r", encoding="utf-8") as file:
        word_replacements = json.load(file)

    modified_text = text
    for key, value in word_replacements.items():
        modified_text = modified_text.replace(key, value)

    response = comprehend.detect_key_phrases(Text=modified_text, LanguageCode="ko")
    key_phrases = [
        phrase["Text"]
        for phrase in response["KeyPhrases"]
        if phrase["Score"] >= min_score
    ]
    return key_phrases


def get_ImageCreator_Cookie():
    try:
        bingCookie = AWSManager.get_secret("BingImageCreator")["cookie"]

        return bingCookie
    except Exception as e:
        raise Exception("BingImageCreator API 키를 가져오는 데 실패했습니다.") from e


def count_keyword(poll_id):
    submits = Submit.objects.filter(poll_id=poll_id)

    keyword_count = [{} for _ in range(fixed_question_num + 1)]

    for submit in submits:
        submit_id = submit.id
        answers = Answer.objects.filter(submit_id=submit_id)
        for i, answer in enumerate(answers, start=1):
            if i <= fixed_question_num:
                if answer.keyword in keyword_count[i]:
                    keyword_count[i][answer.keyword] += 1
                else:
                    keyword_count[i][answer.keyword] = 1

    return keyword_count


def create_submit(poll_id, nick_name, prompt, is_creator):
    poll = Poll.objects.get(id=poll_id)
    user_id = poll.user_id

    submit_data = {
        "user_id": user_id,
        "poll_id": poll_id,
        "result_url": None,
        "nick_name": nick_name,
        "character_id": 0,
    }

    update_submit = None
    # 캐릭터 정보 업데이트
    # (질문 생성자가 생성할 수 있는 캐릭터는 총 2개)
    # 1. 본인이 답변한 키워드로 생성된 캐릭터
    # 2. 중복 키워드로 생성된 캐릭터
    # 그래서 first, last로 구분 가능하다.
    if is_creator:
        print("create submit by creator")

        submit_list = Submit.objects.filter(
            user_id=user_id, poll_id=poll_id, nick_name=None
        ).order_by("created_at")

        if nick_name is None:  # 중복키워드로 캐릭터 만들 경우
            if submit_list.count() > 1:
                update_submit = submit_list.last()
        else:  # 캐릭터 다시 만들 경우
            update_submit = submit_list.first()
        submit_data["nick_name"] = None
        if update_submit:  # 캐릭터 다시 생성 시
            submit_data["character_id"] = update_submit.id

    if update_submit is None:  # 캐릭터 최초 생성 시, 답변자가 생성할 때
        # 캐릭터 정보 저장
        submit_serializer = SubmitCreateSerializer(data=submit_data)
        if submit_serializer.is_valid():
            submit_instance = submit_serializer.save()
        else:
            return Response(
                submit_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        submit_data["character_id"] = submit_instance.id

    # response data 수정
    submit_data.pop("user_id")
    submit_data.pop("poll_id")
    submit_data["keyword"] = prompt

    return submit_data


def create_answer(question_id, submit_id, i, content, keyword):
    data = {
        "question_id": question_id,
        "submit_id": submit_id,
        "num": i + 1,
        "content": content,
        "keyword": keyword,
    }
    answer_serializer = AnswerPostSerializer(data=data)
    if answer_serializer.is_valid():
        answer_serializer.save()
    else:
        return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Characters(APIView):
    @swagger_auto_schema(
        query_serializer=GetCharacterListRequestSerializer,
        responses={200: GetCharacterListResponseSerializer},
    )
    def get(self, request):
        user_id = request.query_params.get("user_id", None)

        if user_id is not None:
            user_id = decrypt_resource_id(user_id)
        elif request.user.is_authenticated:
            user_id = request.user.user_id
        else:
            return Response(
                {"errors": "invalid_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        submit = Submit.objects.filter(user_id=user_id).exclude(result_url__isnull=True).order_by("created_at")

        submit_serializer = SubmitSerializer(submit, many=True)

        # user nick_name 가져오기
        user = User.objects.get(user_id=user_id)

        nick_name = user.nick_name

        user_characters = []
        filtered_data = []

        count = 0
        duplicate_character = None
        for data in submit_serializer.data:
            # 만약 중복 키워드로 생성된 캐릭터 or 본인이 직접 만든 캐릭터일 경우
            if data["nick_name"] is None:
                data["nick_name"] = nick_name
                answer_data = Answer.objects.filter(submit_id=data["id"])
                answer_serializer = AnswerSerializer(answer_data, many=True)

                keyword = []
                for answer in answer_serializer.data:
                    # 답변 번호 1~5(고정질문에 대한 답변)만 키워드로 추출
                    if 1 <= answer["num"] <= fixed_question_num:
                        if answer["keyword"] != "":
                            keyword.append(answer["keyword"])
                    else:
                        break

                # response data에 키워드 추가
                data["keyword"] = keyword
                if count == 0:
                    my_character = data
                if count == 1:
                    duplicate_character = data
                count += 1
                user_characters.append(data)
            else:
                filtered_data.append(data)

            data["id"] = encrypt_resource_id(data["id"])

        # filtered_data = [
        #     character
        #     for character in submit_serializer.data
        #     if character not in user_characters
        # ]

        # for character in user_characters:
        #     character["id"] = encrypt_resource_id(character["id"])

        return Response(
            {
                "nick_name": nick_name,
                "my_character": my_character,
                "duplicate_character": duplicate_character,
                "characters": filtered_data,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=PostCharacterRequestSerializer,
        responses={201: PostCharacterResponseSerializer},
    )
    def post(self, request):
        poll_id = decrypt_resource_id(request.data.get("poll_id"))

        if poll_id is None:
            Response({"errors": "invalid_id"}, status=status.HTTP_400_BAD_REQUEST)

        print("post", poll_id)

        poll = Poll.objects.get(id=poll_id)

        if request.user.is_authenticated and request.user.user_id == poll.user_id:
            is_creator = True
        else:
            is_creator = False

        print("is_creator:", is_creator)

        nick_name = request.data.get("creatorName")
        answers = request.data.get("answers")

        prompt = []

        # 답변 추출
        for i in range(len(answers)):
            temp_answer = answers[i] + " 사용해"

            if i < fixed_question_num:
                keyword = extract_key_phrases(temp_answer)
                print("extracted_keyword:", keyword)
                if len(keyword) == 0 or keyword == temp_answer:
                    keyword = [temp_answer.replace(" 사용해", "")]
                else:
                    keyword
                print("keyword:", keyword)
                # 추출된 키워드 배열
                prompt.extend(keyword)
            else:
                break
        # 캐릭터 생성
        submit_data = create_submit(poll_id, nick_name, prompt, is_creator)
        submit_id = submit_data["character_id"]

        # 이미지 생성 시작(여기서 빈 문자열을 굳이 보낼 필요가 있을까)
        task = create_character.delay(submit_id, prompt)

        # 질문 고유 번호 불러오기
        question = Question.objects.filter(poll_id=poll_id).order_by("id")
        question_id_serializer = QuestionIdSerializer(question, many=True)

        # 캐릭터 아이디로 답변 검색
        answer_list = Answer.objects.filter(submit_id=submit_id).order_by("id")

        print("n_answers, prev:", len(answer_list), "now:", len(answers))

        # 답변 저장
        for i in range(len(answers)):
            content = answers[i]
            if i < fixed_question_num:
                keyword = prompt[i]
            else:
                keyword = None
            question_id = question_id_serializer.data[i]["id"]

            if answer_list:  # 캐릭터에 대한 답변 업데이트
                if len(answer_list) <= i:
                    create_answer(question_id, submit_id, i, content, keyword)
                else:
                    answer_list[i].content = content
                    answer_list[i].keyword = keyword
                    answer_list[i].save()
            else:  # 캐릭터에 대한 답변 생성
                create_answer(question_id, submit_id, i, content, keyword)

        return Response({"task_id": task.id}, status=status.HTTP_201_CREATED)


class URLs(APIView):  # 4개의 캐릭터 url 받아오기
    @swagger_auto_schema(responses={200: GetURLsResponseSerializer})
    def get(self, _, task_id):
        task = AsyncResult(task_id)

        if not task.ready():
            return Response(
                # {"status": task.state}, status=status.HTTP_406_NOT_ACCEPTABLE
                # {"status": task.state},
                status=status.HTTP_202_ACCEPTED,
            )  # status code 수정

        # 롱폴링 구현 필요

        result = task.get()
        if result is not None:
            keyword = result["keyword"]
        else:
            return Response(
                "bing_api error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        while "" in keyword:
            keyword.remove("")

        response_data = {"result_url": task.get()["result_url"], "keyword": keyword}

        return Response(response_data, status=status.HTTP_200_OK)


class FinalSubmit(APIView):
    @swagger_auto_schema(
        request_body=PostFinalSubmitRequestSerializer,
        responses={201: PostFinalSubmitResponseSerializer},
    )
    def post(self, request):  # url선택시 submit에 url 저장
        task_id = request.data.get("task_id")
        index = request.data.get("index")
        task = AsyncResult(task_id)

        result_url = task.get()["result_url"][index]
        submit_id = task.get()["submit_id"]

        final_url = upload_img_to_s3(result_url)

        submit = Submit.objects.get(id=submit_id)
        submit.result_url = final_url
        submit.save()

        return Response(
            {"message": encrypt_resource_id(submit_id)}, status=status.HTTP_201_CREATED
        )


class CharacterDetail(APIView):
    @swagger_auto_schema(responses={200: GetCharacterDetailResponseSerializer})
    def get(self, _, character_id):
        submit_id = decrypt_resource_id(character_id)

        if submit_id is None:
            Response({"errors": "invalid_id"}, status=status.HTTP_400_BAD_REQUEST)

        print(submit_id, type(submit_id))
        try:
            submit = Submit.objects.get(id=submit_id)
        except ObjectDoesNotExist:
            return Response(
                {"error": "submit does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        submit_data = SubmitDetailSerializer(submit)

        # 캐릭터 답변 정보 가져오기
        answer = Answer.objects.filter(submit_id=submit_id)
        answer_data = AnswerSerializer(answer, many=True)

        answers = []
        keyword = []
        for data in answer_data.data:
            answers.append(data["content"])
            if data["keyword"] is not None and data["keyword"] != "":
                keyword.append(data["keyword"])

        # 캐릭터 질문 정보 가져오기
        question = Question.objects.filter(poll_id=submit.poll_id)
        question_data = QuestionTextSerializer(question, many=True)

        questions = []
        for data in question_data.data:
            questions.append(data["question_text"])

        response_data = dict(submit_data.data)
        response_data["id"] = encrypt_resource_id(response_data["id"])
        response_data["questions"] = questions
        response_data["answers"] = answers
        response_data["keyword"] = keyword

        return Response(response_data, status=status.HTTP_200_OK)


class DuplicateCharacter(APIView):
    @swagger_auto_schema(
        request_body=GetCharacterListRequestSerializer,
        responses={201: PostCharacterResponseSerializer},
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            user_id = request.user.user_id
            tmp_user_id = request.data.get("user_id")

        if user_id != tmp_user_id and user_id != decrypt_resource_id(tmp_user_id):
            return Response(
                {"message": "중복캐릭터 생성 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        poll = Poll.objects.filter(user_id=user_id).order_by("created_at").last()

        if poll is None:
            return Response(
                {"message": "질문지를 먼저 작성해 주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        poll_id = poll.id
        keyword_count = count_keyword(poll_id)

        if keyword_count[1] == {}:
            return Response(
                {"message": "아직 답변이 모이지 않았어요!"}, status=status.HTTP_400_BAD_REQUEST
            )

        prompt = []
        for i in range(1, fixed_question_num + 1):
            if keyword_count[i]:
                max_value_keyword = max(keyword_count[i], key=keyword_count[i].get)
                prompt.append(str(max_value_keyword))
            else:
                prompt.append("")  # tmp

        submit_data = create_submit(poll_id, None, prompt, True)
        submit_id = submit_data["character_id"]

        task = create_character.delay(submit_id, prompt, True)

        # 질문 고유 번호 불러오기
        question = Question.objects.filter(poll_id=poll_id)
        question_id_serializer = QuestionIdSerializer(question, many=True)

        answer_list = Answer.objects.filter(submit_id=submit_id).order_by("id")
        print(prompt, len(prompt))
        print(len(question_id_serializer.data))
        # 중복 캐릭터에 대한 답변 저장
        for i in range(len(prompt)):
            keyword = prompt[i]
            if answer_list:  # 캐릭터에 대한 답변 업데이트
                answer_list[i].content = None
                answer_list[i].keyword = keyword
                answer_list[i].save()
            else:
                question_id = question_id_serializer.data[i]["id"]
                data = {
                    "question_id": question_id,
                    "submit_id": submit_id,
                    "num": i + 1,
                    "content": None,
                    "keyword": keyword,
                }
                answer_serializer = AnswerPostSerializer(data=data)
                if answer_serializer.is_valid():
                    answer_serializer.save()
                else:
                    return Response(
                        answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

        return Response({"task_id": task.id}, status=status.HTTP_201_CREATED)


class KeywordChart(APIView):
    @swagger_auto_schema(
        query_serializer=GetCharacterListRequestSerializer,
        responses={200: GetKeywordChartResponseSerializer},
    )
    def get(self, request):
        user_id = request.query_params.get("user_id", None)

        if user_id is not None:
            user_id = decrypt_resource_id(user_id)
        elif request.user.is_authenticated:
            user_id = request.user.user_id
        else:
            return Response(
                {"errors": "invalid_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        poll = Poll.objects.filter(user_id=user_id).order_by("created_at").last()
        poll_id = poll.id
        keyword_count = count_keyword(poll_id)

        if keyword_count[1] == {}:
            return Response(
                {"message": "아직 답변이 모이지 않았어요!"}, status=status.HTTP_400_BAD_REQUEST
            )

        for i in range(fixed_question_num + 1):
            sorted_keyword_count = dict(
                sorted(keyword_count[i].items(), key=lambda x: x[1], reverse=True)
            )

            # 예외 처리 (키가 빈문자열("") 인 경우)
            if "" in sorted_keyword_count.keys():
                del sorted_keyword_count[""]

            for key in sorted_keyword_count:
                sorted_keyword_count[key] = sorted_keyword_count[key]
            keyword_count[i] = {i: sorted_keyword_count}
        keyword_count.pop(0)

        Response_data = {"keyword_count": keyword_count}
        return Response(Response_data, status=status.HTTP_200_OK)


# class CharacterInfo(APIView):
#     @swagger_auto_schema(responses={200: GetCharacterInfoResponseSerializer})
#     def get(self, request, task_id):  # 최종 결과물
#         task = AsyncResult(task_id)
#         submit_id = task.get()["submit_id"]
#         keyword = task.get()["keyword"]

#         submit = Submit.objects.get(id=submit_id)
#         response_data = SubmitSerializer(submit).data
#         response_data["keyword"] = keyword

#         return Response(response_data, status=status.HTTP_200_OK)


# APIView 클래스 정의
class nlpAPI(APIView):
    def get(self, request):
        text = request.GET.get(
            "text", "This is a task sentence for keyword extraction."
        )
        key_phrases = extract_key_phrases(text)

        try:
            # 이미지 생성 및 저장
            start_time = time.time()

            auth_cookie = (
                get_ImageCreator_Cookie()
            )  # BingImageCreator API 인증에 사용되는 쿠키 값 가져오기
            image_generator = ImageGenAPI(auth_cookie)
            image_links = image_generator.get_images(text)

            processing_time = time.time() - start_time
        except Exception as e:
            print(f"Error: {str(e)}")
            # 이미지 생성에 실패한 경우 처리 (e.g., 오류 응답 반환)
            return Response({"error": str(e)})

        # 이미지 생성이 정상적으로 완료된 경우 결과 반환
        return Response(
            {
                "key_phrases": key_phrases,
                "image_links": image_links,
                "processing_time": processing_time,
            }
        )

    def post(self, request):
        text = request.data.get("text", "")
        key_phrases = extract_key_phrases(text)

        try:
            # 이미지 생성 및 저장
            start_time = time.time()

            auth_cookie = (
                get_ImageCreator_Cookie()
            )  # BingImageCreator API 인증에 사용되는 쿠키 값 가져오기
            image_generator = ImageGenAPI(auth_cookie)
            image_links = image_generator.get_images(text)

            processing_time = time.time() - start_time
        except Exception as e:
            print(f"Error: {str(e)}")
            # 이미지 생성에 실패한 경우 처리 (e.g., 오류 응답 반환)
            return Response({"error": str(e)})

        # 이미지 생성이 정상적으로 완료된 경우 결과 반환
        return Response(
            {
                "key_phrases": key_phrases,
                "image_links": image_links,
                "processing_time": processing_time,
            }
        )
