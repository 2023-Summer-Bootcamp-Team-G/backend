from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, login, logout

from drf_yasg.utils import swagger_auto_schema
from .swagger_serializer import (
    PostUserRequestSerializer,
    PostUserResponseSerializer,
    PostLoginRequestSerializer,
    PostLoginResponseSerializer,
)

from question.models import Poll
from common.auth import encrypt_resource_id
from asgiref.sync import sync_to_async
from common.asyncAPIView import AsyncAPIView

User = get_user_model()


class RegisterView(AsyncAPIView):
    @swagger_auto_schema(
        request_body=PostUserRequestSerializer,
        responses={201: PostUserResponseSerializer},
    )
    async def post(self, request):
        nick_name = request.data.get("nick_name")
        user_id = request.data.get("user_id")
        password = request.data.get("password")

        if not nick_name or not user_id or not password:
            return Response(
                {"error": "필수 정보 누락."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if await sync_to_async(lambda: User.objects.filter(user_id=user_id).exists())():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_409_CONFLICT,
            )

        if ":" in user_id:
            return Response(
                {"error": "user_id에 ':'가 포함되었어요! 다른 id를 입력해 주세요!."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User(
            user_id=user_id,
            nick_name=nick_name,
            password=password,
        )

        await sync_to_async(user.save)()
        await sync_to_async(login)(request, user)

        return Response(
            {"message": "User registered successfully."}, status=status.HTTP_201_CREATED
        )


class LoginView(AsyncAPIView):
    @swagger_auto_schema(
        request_body=PostLoginRequestSerializer,
        responses={200: PostLoginResponseSerializer},
    )
    async def post(self, request):
        username = request.data.get("user_id")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = await sync_to_async(authenticate)(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        await sync_to_async(login)(request, user)
        poll = await sync_to_async(lambda: Poll.objects.filter(user_id=user.user_id).order_by("created_at").last())()

        if poll is not None:
            poll_id = encrypt_resource_id(poll.id)
        else:
            poll_id = None

        return Response(
            {
                "user_data": {
                    "nick_name": user.nick_name,
                    "poll_id": poll_id,
                },
                "message": "Login successful.",
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(AsyncAPIView):
    async def post(self, request):
        await sync_to_async(logout)(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
