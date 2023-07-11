from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Question
from .serializer import QuestionSerializer1, QuestionSerializer2, PollSerializer


def create_poll(user_id):
    serializer = PollSerializer(data={"user_id": user_id})
    if serializer.is_valid():
        poll = serializer.save()
        return poll.id
    else:
        return None


@api_view(["POST"])
def question(request):
    user_id = request.query_params.get("user_id")
    poll_id = create_poll(user_id)  # poll 생성

    if poll_id is None:
        return Response({"error": "poll 생성 실패"}, status=status.HTTP_400_BAD_REQUEST)

    updated_questions = []

    # 질문 내용 체크 및 직렬화
    questions_serializer = QuestionSerializer1(
        data=request.data["questions"], many=True
    )
    if questions_serializer.is_valid():
        questions = questions_serializer.validated_data
        # 데이터베이스에 저장할 질문 데이터 생성
        for index, question in enumerate(questions):
            question["poll_id"] = poll_id
            question["question_number"] = index + 1
            updated_questions.append(question)
    else:
        return Response(
            {"errors": questions_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # 데이터(질문) 저장 및 응답 정보 생성
    updated_serializer = QuestionSerializer2(data=updated_questions, many=True)
    response_data = []
    if updated_serializer.is_valid():
        updated_questions = updated_serializer.save()
        for question in updated_questions:
            response_data.append(
                {
                    "question_id": question.question_number,
                    "question_text": question.question_text,
                }
            )
    else:
        return Response(
            {"error": updated_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    response = {"questions": response_data}
    return Response(response, status=status.HTTP_201_CREATED)
