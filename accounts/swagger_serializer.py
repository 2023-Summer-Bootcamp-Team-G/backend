from rest_framework import serializers


class PostUserRequestSerializer(serializers.Serializer):
    nick_name = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()


class PostUserResponseSerializer(serializers.Serializer):
    message = serializers.CharField()