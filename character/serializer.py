from rest_framework import serializers
from .models import Submit, Answer

class SubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ['id', 'result_url', 'nick_name']

class SubmitDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ['id', 'result_url', 'nick_name']
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['num', 'content']