from rest_framework import serializers
from .models import Question, Poll


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ["user_id"]


class QuestionSerializer(serializers.Serializer):  # 질문 내용만 체크
    questions = serializers.ListField(child=serializers.CharField())


class UpdatedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["poll_id", "question_number", "question_text"]


class QuestionTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["question_text"]


class QuestionIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id"]
