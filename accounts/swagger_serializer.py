from rest_framework import serializers


class PostUserRequestSerializer(serializers.Serializer):
    nick_name = serializers.CharField()
    user_id = serializers.CharField()
    password = serializers.CharField()


class PostUserResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class PostLoginRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()


class PostLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
