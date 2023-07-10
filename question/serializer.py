from rest_framework import serializers
from .models import Question, Poll

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['user_id']

class QuestionSerializer1(serializers.ModelSerializer): # 질문 내용만 체크
    class Meta:
        model = Question
        fields = ['question_text']

class QuestionSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['poll_id', 'question_number', 'question_text']

class QuestionSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_number', 'question_text']