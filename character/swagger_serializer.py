from rest_framework import serializers


class GetCharacterListRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class CharacterInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    result_url = serializers.CharField()
    nick_name = serializers.CharField()
    keyword = serializers.ListField()


class GetCharacterListResponseSerializer(serializers.Serializer):
    characters = CharacterInfoSerializer(many=True)
    

class QuestionInfoSerializer(serializers.Serializer):
    question_number = serializers.IntegerField()
    question_text = serializers.CharField()


class AnswerInfoSerializer(serializers.Serializer):
    num = serializers.IntegerField()
    content = serializers.CharField()


class GetCharacterDetailResponseSerializer(serializers.Serializer):
    character_id = serializers.IntegerField()
    result_url = serializers.CharField()
    nick_name = serializers.CharField()
    questions = QuestionInfoSerializer(many=True)
    answers = AnswerInfoSerializer(many=True)