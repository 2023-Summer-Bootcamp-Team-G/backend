from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

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

        return Response({"message": "Login successful."},
                        tatus=status.HTTP_200_OK)
