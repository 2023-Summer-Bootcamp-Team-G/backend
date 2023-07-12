from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Submit, Answer
from question.models import Question, Poll
from .serializer import (
    SubmitSerializer,
    SubmitDetailSerializer,
    SubmitCreateSerializer,
    AnswerSerializer,
    AnswerPostSerializer,
)
from question.serializer import QuestionSerializer3

fixed_question_num = 3


def extract_keyword(answer):
    return "키워드"


def create_image(prompt):
    url = "https://exapmle.com/"
    return url


# def create_submit(poll_id, nick_name, prompt):
# result_url = create_image(prompt)

# poll = Poll.objects.get(id=poll_id)
# user_id = poll.user_id

# submit_data = {'user_id': user_id, 'poll_id': poll_id, 'result_url': result_url, 'nick_name': nick_name}

# submit_serializer = SubmitCreateSerializer(data=submit_data)
# if submit_serializer.is_valid():
#     submit_serializer.save()
# else:
#     return Response(submit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# submit_data['character_id'] = submit_serializer.data['id']

# return submit_data


class Characters(APIView):
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

    def post(self, request):
        poll_id = request.query_params.get("poll_id")
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
        result_url = create_image(prompt)

        poll = Poll.objects.get(id=poll_id)
        user_id = poll.user_id.id

        submit_data = {
            "user_id": user_id,
            "poll_id": poll_id,
            "result_url": result_url,
            "nick_name": nick_name,
        }

        submit_serializer = SubmitCreateSerializer(data=submit_data)
        if submit_serializer.is_valid():
            submit_instance = submit_serializer.save()
        else:
            return Response(
                submit_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        submit_data["character_id"] = submit_instance.id
        submit_id = submit_data["character_id"]

        # 답변 저장
        for i, answer in enumerate(answers, start=1):
            if i <= fixed_question_num:
                keyword = prompt[i - 1]
            else:
                keyword = answer["answer_text"]

            question_id = answer["question_id"]
            data = {
                "question_id": question_id,
                "submit_id": submit_id,
                "num": i,
                "content": keyword,
            }
            answer_serializer = AnswerPostSerializer(data=data)
            if answer_serializer.is_valid():
                answer_serializer.save()
            else:
                return Response(
                    answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        # response data 수정
        submit_data.pop("user_id")
        submit_data.pop("poll_id")
        submit_data["keyowrd"] = prompt

        return Response(submit_data, status=status.HTTP_201_CREATED)


class CharacterDetail(APIView):
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
