from rest_framework import serializers


class PostQuestionRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    questions = serializers.ListField(child=serializers.CharField())


class PostQuestionResponseSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()


class GetQuestionRequestSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()


class GetQuestionResponseSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    nick_name = serializers.CharField()
    questions = serializers.ListField(child=serializers.CharField())
