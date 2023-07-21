from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# from gTeamProject.settings import extract_key_phrases
from aws import AWSManager

import os
from dotenv import load_dotenv
from django.conf import settings

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
)
from .task import create_character
from celery.result import AsyncResult

import random

fixed_question_num = 2

# # .env.dev 파일 로드
# load_dotenv(dotenv_path)

# AWS Comprehend 클라이언트를 생성
comprehend = AWSManager._session.client("comprehend")  # 임시 설정 AWSManager._session


def extract_key_phrases(text):
    text_encoded = text.encode("utf-8").decode("unicode_escape")
    response = comprehend.detect_key_phrases(Text=text_encoded, LanguageCode="en")
    key_phrases = [phrase["Text"] for phrase in response["KeyPhrases"]]
    return key_phrases


class nlpAPI(APIView):
    def get(self, request):
        text = request.GET.get("text", "")
        key_phrases = extract_key_phrases(text)
        return JsonResponse({"key_phrases": key_phrases})

    def post(self, request):
        text = request.data.get("text", "")
        key_phrases = extract_key_phrases(text)
        return JsonResponse({"key_phrases": key_phrases})


def get_user_data(request):
    session_id = request.session.session_key
    user_id = request.session.get("user_id")
    nick_name = request.session.get("nick_name")

    if user_id and nick_name:
        return True
        # user_data = {
        #     "session_id": session_id,
        #     "user_id": user_id,
        #     "nick_name": nick_name,
        # }
    else:
        return False
        # user_data = {
        #     "session_id": session_id,
        #     "user_id": None,
        #     "nick_name": None,
        # }

    # return JsonResponse(user_data)


def extract_keyword(answer):
    keyword = ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"]
    num = random.randint(0, 4)
    return keyword[num]


def create_submit(poll_id, nick_name, prompt, login):
    # result_url = create_image(prompt)

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
    if login:
        submit_list = Submit.objects.filter(
            user_id=user_id, poll_id=poll_id, nick_name=None
        ).order_by("created_at")

        if nick_name == None:  # 중복키워드로 캐릭터 만들 경우
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


class Characters(APIView):
    @swagger_auto_schema(
        query_serializer=GetCharacterListRequestSerializer,
        responses={200: GetCharacterListResponseSerializer},
    )
    def get(self, request):
        # 캐릭터 정보 가져오기
        user_id = request.query_params.get("user_id")
        submit = Submit.objects.filter(user_id=user_id)
        submit_serializer = SubmitSerializer(submit, many=True)

        # user nick_name 가져오기
        user = User.objects.get(user_id=user_id)
        nick_name = user.nick_name

        user_characters = []

        for data in submit_serializer.data:
            # 만약 중복 키워드로 생성된 캐릭터 or 본인이 직접 만든 캐릭터일 경우
            if data["nick_name"] == None:
                data["nick_name"] = nick_name
                answer_data = Answer.objects.filter(submit_id=data["id"])
                answer_serializer = AnswerSerializer(answer_data, many=True)

                keyword = []
                for answer in answer_serializer.data:
                    # 답변 번호 1~5(고정질문에 대한 답변)만 키워드로 추출
                    if 1 <= answer["num"] <= fixed_question_num:
                        keyword.append(answer["content"])
                    else:
                        break
                # response data에 키워드 추가
                data["keyword"] = keyword
                user_characters.append(data)

        filtered_data = [
            character
            for character in submit_serializer.data
            if character not in user_characters
        ]

        user_characters.extend(filtered_data)

        response_data = {"characters": user_characters}
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PostCharacterRequestSerializer,
        responses={201: PostCharacterResponseSerializer},
    )
    def post(self, request):
        login = get_user_data(request)
        poll_id = request.data.get("poll_id")
        nick_name = request.data.get("creatorName")
        answers = request.data.get("answers")

        prompt = []

        # 답변 추출
        for i in range(len(answers)):
            if i < fixed_question_num:
                keyword = extract_keyword(answers[i])
                # 추출된 키워드 배열
                prompt.append(keyword)
            else:
                break
        # 캐릭터 생성
        submit_data = create_submit(poll_id, nick_name, prompt, login)
        submit_id = submit_data["character_id"]

        # 이미지 생성 시작
        task = create_character.delay(submit_id, prompt)

        # 질문 고유 번호 불러오기
        question = Question.objects.filter(poll_id=poll_id).order_by("id")
        question_id_serializer = QuestionIdSerializer(question, many=True)

        # 캐릭터 아이디로 답변 검색
        answer_list = Answer.objects.filter(submit_id=submit_id).order_by("id")

        # 답변 저장
        for i in range(len(answers)):
            if i < fixed_question_num:
                keyword = prompt[i]
            else:
                keyword = answers[i]

            question_id = question_id_serializer.data[i]["id"]

            if answer_list:  # 캐릭터에 대한 답변 업데이트
                answer_list[i].content = keyword
                answer_list[i].save()
            else:  # 캐릭터에 대한 답변 생성
                data = {
                    "question_id": question_id,
                    "submit_id": submit_id,
                    "num": i + 1,
                    "content": keyword,
                }
                answer_serializer = AnswerPostSerializer(data=data)
                if answer_serializer.is_valid():
                    answer_serializer.save()
                else:
                    return Response(
                        answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

        return Response({"task_id": task.id}, status=status.HTTP_201_CREATED)


class CharacterDetail(APIView):
    @swagger_auto_schema(responses={200: GetCharacterDetailResponseSerializer})
    def get(self, request, character_id):
        try:
            # 캐릭터 상세 정보 가져오기
            submit = Submit.objects.get(id=character_id)
        except ObjectDoesNotExist:
            return Response(
                {"error": "submit does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        submit_data = SubmitDetailSerializer(submit)

        # 캐릭터 답변 정보 가져오기
        answer = Answer.objects.filter(submit_id=character_id)
        answer_data = AnswerSerializer(answer, many=True)

        # 캐릭터 질문 정보 가져오기
        question = Question.objects.filter(poll_id=submit.poll_id)
        question_data = QuestionTextSerializer(question, many=True)

        response_data = dict(submit_data.data)
        response_data["questions"] = question_data.data
        response_data["answers"] = answer_data.data

        return Response(response_data, status=status.HTTP_200_OK)


def count_keyword(poll_id):
    submits = Submit.objects.filter(poll_id=poll_id)

    keyword_count = [{} for _ in range(fixed_question_num + 1)]

    for submit in submits:
        submit_id = submit.id
        answers = Answer.objects.filter(submit_id=submit_id)
        for i, answer in enumerate(answers, start=1):
            if i <= fixed_question_num:
                if answer.content in keyword_count[i]:
                    keyword_count[i][answer.content] += 1
                else:
                    keyword_count[i][answer.content] = 1

    return keyword_count


class DuplicateCharacter(APIView):
    @swagger_auto_schema(
        request_body=GetCharacterListRequestSerializer,
        responses={201: PostCharacterResponseSerializer},
    )
    def post(self, request):
        login = get_user_data(request)
        if login == False:
            return Response(
                {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        user_id = request.data.get("user_id")

        poll = Poll.objects.filter(user_id=user_id).order_by("created_at").last()
        poll_id = poll.id
        keyword_count = count_keyword(poll_id)

        if keyword_count[1] == {}:
            return Response(
                {"message": "아직 답변이 모이지 않았어요!"}, status=status.HTTP_400_BAD_REQUEST
            )

        prompt = []
        for i in range(1, fixed_question_num + 1):
            max_value_keyword = max(keyword_count[i], key=keyword_count[i].get)
            prompt.append(max_value_keyword)

        submit_data = create_submit(poll_id, None, prompt, login)
        submit_id = submit_data["character_id"]

        task = create_character.delay(submit_id, prompt)

        # 질문 고유 번호 불러오기
        question = Question.objects.filter(poll_id=poll_id)
        question_id_serializer = QuestionIdSerializer(question, many=True)

        # 중복 캐릭터에 대한 답변 저장
        for i in range(len(prompt)):
            keyword = prompt[i]

            question_id = question_id_serializer.data[i]["id"]
            data = {
                "question_id": question_id,
                "submit_id": submit_id,
                "num": i + 1,
                "content": keyword,
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
        user_id = request.query_params.get("user_id")

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
            total = sum(sorted_keyword_count.values())
            for key in sorted_keyword_count:
                sorted_keyword_count[key] = [sorted_keyword_count[key]]
                sorted_keyword_count[key].append(
                    round(sorted_keyword_count[key][0] / total * 100, 2)
                )
            keyword_count[i] = {i: sorted_keyword_count}
        keyword_count.pop(0)

        Response_data = {"keyword_count": keyword_count}
        return Response(Response_data, status=status.HTTP_200_OK)


class Task(APIView):
    def get(self, request, task_id):
        task = AsyncResult(task_id)
        if not task.ready():
            return Response(
                {"status": task.state}, status=status.HTTP_406_NOT_ACCEPTABLE
            )  # status code 수정

        #         response_data = task.get()["submit_data"] # DB 에서 조회
        submit_id = task.get()["submit_id"]
        keyword = task.get()["keyword"]

        submit = Submit.objects.get(id=submit_id)
        response_data = SubmitSerializer(submit).data
        response_data["keyword"] = keyword

        return Response(response_data, status=status.HTTP_200_OK)
