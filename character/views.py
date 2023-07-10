from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http import JsonResponse 
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Submit, Answer
from question.models import Question
from user.models import User
from .serializer import SubmitSerializer, SubmitDetailSerializer, AnswerSerializer
from question.serializer import QuestionSerializer3

class Characters(APIView):
    def get(self, request):
        pass
        

class CharacterDetail(APIView):
    def get(self, request, character_id):
        #캐릭터 상세 정보 가져오기
        submit = Submit.objects.get(id=character_id)
        submit_data = SubmitDetailSerializer(submit)
        
        #캐릭터 답변 정보 가져오기
        answer = Answer.objects.filter(submit_id=character_id)
        answer_data = AnswerSerializer(answer, many=True)
        
        #캐릭터 질문 정보 가져오기
        question = Question.objects.filter(poll_id=submit.poll_id)
        question_data = QuestionSerializer3(question, many=True)
        
        response_data = dict(submit_data.data)
        response_data['questions'] = question_data.data
        response_data['answers'] = answer_data.data
        
        return Response(response_data, status=status.HTTP_200_OK)