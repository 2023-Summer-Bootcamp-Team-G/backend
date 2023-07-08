from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http import JsonResponse 
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Submit, Answer
from question.models import Question
from user.models import User
from .serializer import SubmitSerializer

class Character(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        submit = Submit.objects.filter(id=user_id)
        submit_serializer = SubmitSerializer(submit, many=True)
        user_nick_name = User.objects.get(id=user_id).nick_name
        response_data = {"characters": submit_serializer.data, "user_nick_name": user_nick_name}
        Response(response_data, status=status.HTTP_200_OK)
        
        