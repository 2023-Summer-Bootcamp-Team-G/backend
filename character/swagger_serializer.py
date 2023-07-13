from rest_framework import serializers


class GetCharacterListRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField()


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


class AnswerInfoSerializer2(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_text = serializers.CharField()


class PostCharacterRequestSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()
    creatorName = serializers.CharField()
    answers = AnswerInfoSerializer2(many=True)


class PostCharacterResponseSerializer(serializers.Serializer):
    result_url = serializers.CharField()
    nick_name = serializers.CharField()
    character_id = serializers.IntegerField()
    keyword = serializers.ListField()


class KeywordCountSerializer(serializers.Serializer):
    keyword = serializers.IntegerField()


class KeywordNumberSerializer(serializers.Serializer):
    num = KeywordCountSerializer(many=True)


class GetKeywordChartResponseSerializer(serializers.Serializer):
    keyword_count = KeywordNumberSerializer(many=True)