from rest_framework import status
from rest_framework.views import APIView
from django.views import View
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

        user.save()

        login(request, user)

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

        login(request, user)

        nick_name = user.nick_name
        poll_id = (
            Poll.objects.filter(user_id=user.user_id).order_by("created_at").last().id
        )

        print(poll_id)

        return Response(
            {
                "user_data": {
                    "nick_name": nick_name,
                    "poll_id": encrypt_resource_id(poll_id),
                },
                "message": "Login successful.",
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
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
