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


class GetCharacterDetailResponseSerializer(serializers.Serializer):
    character_id = serializers.IntegerField()
    result_url = serializers.CharField()
    nick_name = serializers.CharField()
    questions = serializers.ListField(child=serializers.CharField())
    answers = serializers.ListField(child=serializers.CharField())
    keyword = serializers.ListField(child=serializers.CharField())


class PostCharacterRequestSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()
    creatorName = serializers.CharField()
    answers = serializers.ListField(child=serializers.CharField())


class PostCharacterResponseSerializer(serializers.Serializer):
    task_id = serializers.CharField()


class KeywordCountSerializer(serializers.Serializer):
    keyword = serializers.ListField()


class KeywordNumberSerializer(serializers.Serializer):
    num = KeywordCountSerializer(many=True)


class GetKeywordChartResponseSerializer(serializers.Serializer):
    keyword_count = KeywordNumberSerializer(many=True)


class GetURLsResponseSerializer(serializers.Serializer):
    result_url = serializers.ListField()
    keyword = serializers.ListField(child=serializers.CharField())


class GetCharacterInfoResponseSerializer(serializers.Serializer):
    result_url = serializers.CharField()
    nick_name = serializers.CharField()
    character_id = serializers.IntegerField()
    keyword = serializers.ListField()


class PostFinalSubmitRequestSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    index = serializers.IntegerField()


class PostFinalSubmitResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
