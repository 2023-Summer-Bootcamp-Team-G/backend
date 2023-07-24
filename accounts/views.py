from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
import requests

# from django.contrib.sessions.backends.db import SessionStore
# from django.views.decorators.csrf import csrf_protect

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


class KakaoSignInView(View):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri = "http://127.0.0.1:8000/sign-in/kakao/callback/"
        client_id = "c0a747f67ed13f79de992cbcdedec359"

        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


class KakaoSignInCallbackView(View):
    def get(self, request):
        try:
            # Get the authorization code from the request parameters
            code = request.GET.get("code")
            client_id = "c0a747f67ed13f79de992cbcdedec359"
            redirect_uri = "http://127.0.0.1:8000/sign-in/kakao/callback/"

            # Use the authorization code to request access token from Kakao
            token_request = requests.get(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )
            token_json = token_request.json()
            print(token_json)

            error = token_json.get("error", None)

            if error is not None:
                return JsonResponse({"message": "INVALID_CODE"}, status=400)

            access_token = token_json.get("access_token")

            # Return the access token in the response
            return JsonResponse({'access_token': access_token}, status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        except access_token.DoesNotExist:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
