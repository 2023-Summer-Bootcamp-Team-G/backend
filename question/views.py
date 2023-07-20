from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import (
    QuestionSerializer,
    UpdatedQuestionSerializer,
    QuestionTextSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from .swagger_serializer import (
    PostQuestionRequestSerializer,
    PostQuestionResponseSerializer,
    GetQuestionResponseSerializer,
    GetQuestionRequestSerializer,
)
from question.models import Poll, Question
from accounts.models import User


def create_poll(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        poll = Poll.objects.create(user=user)
        return poll.id
    except User.DoesNotExist:
        return None


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
    
    
class Questions(APIView):
    @swagger_auto_schema(
        query_serializer=GetQuestionRequestSerializer,
        responses={200: GetQuestionResponseSerializer},
    )
    def get(self, request):
        poll_id = request.GET.get("poll_id")
        poll = Poll.objects.get(id=poll_id)
        questions = Question.objects.filter(poll_id=poll)

        questions_serializer = QuestionTextSerializer(questions, many=True)
        response_data = [item["question_text"] for item in questions_serializer.data]
        response = {"questions": response_data}
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PostQuestionRequestSerializer,
        responses={201: PostQuestionResponseSerializer},
    )
    def post(self, request):
        login = get_user_data(request)
        if not login:
            return Response({"error": "로그인 필요"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = request.data.get("user_id")
        poll_id = create_poll(user_id)  # poll 생성

        if poll_id is None:
            return Response({"error": "poll 생성 실패"}, status=status.HTTP_400_BAD_REQUEST)

        updated_questions = []

        # 질문 내용 체크 및 직렬화
        questions_serializer = QuestionSerializer(data=request.data)
        if questions_serializer.is_valid():
            questions = questions_serializer.validated_data["questions"]
            # 데이터베이스에 저장할 질문 데이터 생성
            for index in range(len(questions)):
                question = {
                    "poll_id": poll_id,
                    "question_number": index + 1,
                    "question_text": questions[index],
                }
                updated_questions.append(question)
        else:
            return Response(
                {"errors": questions_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 데이터(질문) 저장
        updated_serializer = UpdatedQuestionSerializer(
            data=updated_questions, many=True
        )
        if updated_serializer.is_valid():
            updated_serializer.save()
        else:
            return Response(
                {"error": updated_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        response = {"poll_id": poll_id}
        return Response(response, status=status.HTTP_201_CREATED)
