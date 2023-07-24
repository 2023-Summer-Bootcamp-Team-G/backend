from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_protect

# authenticate는 사용자 인증을 수행하는 내장함수, 인증 자격증명(사용자 id, 비밀번호)을
# 사용하여 사용자 인증, 인증에 성공한 경우 사용자 객체 반환, 실패한 경우 `none` 반환
# login은 인증된 사용즈랄 로그인 처리, 세션 관리, 필요 데이터 저장해서
# 사용자를 로그인 상태로 유지하는 내장 함수

from drf_yasg.utils import swagger_auto_schema
from .swagger_serializer import (
    PostUserRequestSerializer,
    PostUserResponseSerializer,
    PostLoginRequestSerializer,
    PostLoginResponseSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=PostUserRequestSerializer,
        responses={201: PostUserResponseSerializer},
    )
    def post(self, request):
        nick_name = request.data.get("nick_name")
        user_id = request.data.get("user_id")
        password = request.data.get("password")

        if not nick_name or not user_id or not password:
            return Response(
                {"error": "필수 정보 누락."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(user_id=user_id).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # User 생성
        user = User(
            user_id=user_id,
            nick_name=nick_name,
            password=password,
        )
        user.save()

        return Response(
            {"message": "User registered successfully."}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=PostLoginRequestSerializer,
        responses={200: PostLoginResponseSerializer},
    )
    def post(self, request):
        username = request.data.get("user_id")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 사용자 정보를 세션에 저장
        request.session["user_id"] = user.user_id
        request.session["nick_name"] = user.nick_name

        # 세션 ID를 클라이언트에게 전송
        response = Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        response.set_cookie(
            "sessionid",
            request.session.session_key,
            httponly=True,
            # secure=True,
            samesite="Lax",
        )

        return response


class LogoutView(APIView):
    def post(self, request):
        # 세션 삭제
        request.session.flush()
        # 사용자 정보 초기화
        request.session["user_id"] = None
        request.session["nick_name"] = None

        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
