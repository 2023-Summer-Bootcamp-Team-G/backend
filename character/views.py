from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

# from gTeamProject.settings import extract_key_phrases
from aws import AWSManager

import os
from dotenv import load_dotenv
from django.conf import settings

from .models import Submit, Answer
from question.models import Question, Poll
from .serializer import (
    SubmitSerializer,
    SubmitDetailSerializer,
    AnswerSerializer,
)
from question.serializer import QuestionSerializer3

from drf_yasg.utils import swagger_auto_schema
from .swagger_serializer import (
    GetCharacterListResponseSerializer,
    GetCharacterListRequestSerializer,
    GetCharacterDetailResponseSerializer,
    PostCharacterRequestSerializer,
    PostCharacterResponseSerializer,
    GetKeywordChartResponseSerializer,
)
from .tasks import create_character
from .utils import extract_keyword, create_submit
from .utils import fixed_question_num
from celery.result import AsyncResult

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


# def extract_keyword(answer):
#     keyword = ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"]
#     num = random.randint(0, 4)
#     return keyword[num]


# def create_image(prompt):
#     url = "https://exapmle.com/"
#     return url


# def create_submit(poll_id, nick_name, prompt):
#     result_url = create_image(prompt)

#     poll = Poll.objects.get(id=poll_id)
#     user_id = poll.user_id

#     submit_data = {
#         "user_id": user_id,
#         "poll_id": poll_id,
#         "result_url": result_url,
#         "nick_name": nick_name,
#     }

#     submit_serializer = SubmitCreateSerializer(data=submit_data)
#     if submit_serializer.is_valid():
#         submit_instance = submit_serializer.save()
#     else:
#         return Response(submit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     submit_data["character_id"] = submit_instance.id

#     # response data 수정
#     submit_data.pop("user_id")
#     submit_data.pop("poll_id")
#     submit_data["keyowrd"] = prompt

#     return submit_data


# def create_answer(submit_id, prompt, answers):
#     for i, answer in enumerate(answers, start=1):
#         if i <= fixed_question_num:
#             keyword = prompt[i - 1]
#         else:
#             keyword = answer["answer_text"]

#         question_id = answer["question_id"]
#         data = {
#             "question_id": question_id,
#             "submit_id": submit_id,
#             "num": i,
#             "content": keyword,
#         }
#         answer_serializer = AnswerPostSerializer(data=data)
#         if answer_serializer.is_valid():
#             answer_serializer.save()
#         else:
#             return Response(
#                 answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
#             )


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

        for data in submit_serializer.data:
            # 만약 중복 키워드로 생성된 캐릭터 or 본인이 직접 만든 캐릭터일 경우
            if data["nick_name"] == None:
                answer_data = Answer.objects.filter(submit_id=data["id"])
                answer_serializer = AnswerSerializer(answer_data, many=True)

                keyword = []
                for answer in answer_serializer.data:
                    # 답변 번호 1~5(고정질문에 대한 답변)만 키워드로 추출
                    if 1 <= answer["num"] <= fixed_question_num:
                        keyword.append(answer["content"])
                # response data에 키워드 추가
                data["keyword"] = keyword

        response_data = {"characters": submit_serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PostCharacterRequestSerializer,
        responses={201: PostCharacterResponseSerializer},
    )
    def post(self, request):
        poll_id = request.data.get("poll_id")
        nick_name = request.data.get("creatorName")
        answers = request.data.get("answers")

        prompt = []

        # 답변 추출
        for i, answer in enumerate(answers, start=1):
            if i <= fixed_question_num:
                keyword = extract_keyword(answer)
                # 추출된 키워드 배열
                prompt.append(keyword)
            else:
                break

        # 캐릭터 생성
        # submit_data = create_submit(poll_id, nick_name, prompt)
        # submit_id = submit_data["character_id"]
        # # 답변 저장
        # create_answer(submit_id, prompt, answers)
        # return Response(submit_data, status=status.HTTP_201_CREATED)
        task = create_character.delay(poll_id, nick_name, prompt, answers)
        return Response({"task_id": task.id}, status=status.HTTP_201_CREATED)


class CharacterDetail(APIView):
    @swagger_auto_schema(responses={200: GetCharacterDetailResponseSerializer})
    def get(self, request, character_id):
        # 캐릭터 상세 정보 가져오기
        submit = Submit.objects.get(id=character_id)
        submit_data = SubmitDetailSerializer(submit)

        # 캐릭터 답변 정보 가져오기
        answer = Answer.objects.filter(submit_id=character_id)
        answer_data = AnswerSerializer(answer, many=True)

        # 캐릭터 질문 정보 가져오기
        question = Question.objects.filter(poll_id=submit.poll_id)
        question_data = QuestionSerializer3(question, many=True)

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
        user_id = request.data.get("user_id")

        poll = Poll.objects.filter(user_id=user_id).order_by("created_at").last()
        poll_id = poll.id
        keyword_count = count_keyword(poll_id)

        prompt = []
        for i in range(1, fixed_question_num + 1):
            max_value_keyword = max(keyword_count[i], key=keyword_count[i].get)
            prompt.append(max_value_keyword)

        submit_data = create_submit(poll_id, None, prompt)

        return Response(submit_data, status=status.HTTP_201_CREATED)


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
            return Response({"status": task.state}, status=status.HTTP_200_OK)

        response_data = task.get()["submit_data"]
        return Response(response_data, status=status.HTTP_200_OK)