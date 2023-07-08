from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http import JsonResponse 
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Submit, Answer
from question.models import Question
from user.models import User
from .serializer import SubmitSerializer, SubmitDetailSerializer, AnswerSerializer

class Characters(APIView):
    def get(self, request):
        #캐릭터 정보 가져오기
        user_id = request.query_params.get('user_id')
        if user_id is None:
            return Response({'error': 'user_id가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        submit = Submit.objects.filter(id=user_id)
        submit_serializer = SubmitSerializer(submit, many=True)
        
        for data in submit_serializer.data:
            # 만약 중복 키워드로 생성된 캐릭터 or 본인이 직접 만든 캐릭터일 경우
            if data['duplicate'] == True or data['nick_name'] == None:
                answer_data = Answer.objects.filter(submit_id=data['id'])
                keyword = []
                for answer in answer_data:
                    # 답변 번호 1~5(고정질문에 대한 답변)만 키워드로 추출
                    if 1<= answer['num'] <= 5:
                        keyword.append(answer['content'])
                #키워드 추가
                data['keyword'] = keyword
        
        #유저 닉네임 가져오기(nick_name = NULL 일 시 활용하기 위함)
        user_nick_name = User.objects.get(id=user_id).nick_name
        if user_nick_name is None:
            return Response({'error': 'user_nic_name가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {"characters": submit_serializer.data, "user_nick_name": user_nick_name}
        Response(response_data, status=status.HTTP_200_OK)
        

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
        
        
        
        
        