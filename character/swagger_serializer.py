from rest_framework import serializers


# class KeywordSerializer(serializers.Serializer):
#     keyword = serializers.ListField()
class GetCharacterListRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class CharacterInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    result_url = serializers.CharField()
    nick_name = serializers.CharField()
    keyword = serializers.ListField()


class GetCharacterListResponseSerializer(serializers.Serializer):
    characters = CharacterInfoSerializer(many=True)