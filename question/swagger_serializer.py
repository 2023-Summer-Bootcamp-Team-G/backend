from rest_framework import serializers


class QuestionTextSerializer1(serializers.Serializer):
    question_text = serializers.CharField()


class PostQuestionRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    questions = QuestionTextSerializer1(many=True)


class QuestionIdTextSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    question_text = serializers.CharField()


class PostQuestionResponseSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()
    questions = QuestionIdTextSerializer(many=True)


class GetQuestionRequestSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()


class GetQuestionResponseSerializer(serializers.Serializer):
    questions = QuestionIdTextSerializer(many=True)