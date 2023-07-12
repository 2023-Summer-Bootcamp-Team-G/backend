from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views import View
from django.conf import settings
import requests

User = get_user_model()


class KakaoLoginView(View):
    def get(self, request):
        # app_key = settings.KAKAO_APP_KEY
        redirect_uri = request.build_absolute_uri("/accounts/login/kakao/callback/")
        authorization_url = f"https://kauth.kakao.com/oauth/authorize?client_id={app5c705df135a44f59c9b017be25864e0b_key}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(authorization_url)


class KakaoCallbackView(View):
    def get(self, request):
        app_key = settings.KAKAO_APP_KEY
        code = request.GET.get("code")
        redirect_uri = request.build_absolute_uri("/accounts/login/kakao/callback/")
        token_url = "https://kauth.kakao.com/oauth/token"
        token_data = {
            "grant_type": "authorization_code",
            "client_id": app_key,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        response = requests.post(token_url, data=token_data)
        response_data = response.json()
        access_token = response_data.get("access_token")

        profile_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = requests.get(profile_url, headers=headers)
        profile_data = profile_response.json()
        kakao_id = profile_data.get("id")
        nickname = profile_data.get("properties", {}).get("nickname")


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        nickname = request.data.get("nickname")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            username=username, password=password, nickname=nickname
        )
        return Response(
            {"message": "User registered successfully."}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
