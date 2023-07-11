from rest_framework import serializers
from .models import Submit, Answer
from question.models import Question
from question.serializer import QuestionSerializer3

class SubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ['id', 'result_url', 'nick_name']

class SubmitDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ['id', 'result_url', 'nick_name']

class SubmitCreatelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ['user_id','poll_id', 'result_url', 'nick_name']
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['num', 'content']
        
class AnswerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question_id', 'num', 'content']