from rest_framework import serializers
from .models import Submit, Answer


class SubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ["id", "result_url", "nick_name"]


class SubmitDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ["id", "result_url", "nick_name"]


class SubmitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ["user_id", "poll_id", "result_url", "nick_name"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["num", "content", "keyword"]


class AnswerPostSerializer(serializers.ModelSerializer):
    keyword = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Answer
        fields = ["question_id", "submit_id", "num", "content", "keyword"]
