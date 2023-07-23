from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
# authenticate는 사용자 인증을 수행하는 내장함수, 인증 자격증명(사용자 id, 비밀번호)을
# 사용하여 사용자 인증, 인증에 성공한 경우 사용자 객체 반환, 실패한 경우 `none` 반환
# login은 인증된 사용즈랄 로그인 처리, 세션 관리, 필요 데이터 저장해서
# 사용자를 로그인 상태로 유지하는 내장 함수

User = get_user_model()


class RegisterView(APIView):
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
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
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

        login(request, user)

        return Response(
            {"message": "Login successful."},
            status=status.HTTP_200_OK
        )


class KakaoView(APIView):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri = "http://127.0.0.1:8000/"
        client_id = "c0a747f67ed13f79de992cbcdedec359"

        return redirect(f"{kakao_api}&client_id={client_id}&redircet_uri={redirect_uri}")
