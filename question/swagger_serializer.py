from rest_framework import serializers


class PostQuestionRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    questions = serializers.ListField(child=serializers.CharField())


class QuestionIdTextSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    question_text = serializers.CharField()


class PostQuestionResponseSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()


class GetQuestionRequestSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()


class GetQuestionResponseSerializer(serializers.Serializer):
    questions = serializers.ListField(child=serializers.CharField())
