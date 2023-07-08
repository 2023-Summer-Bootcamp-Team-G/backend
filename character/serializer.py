from rest_framework import serializers
from .models import Submit, Answer

class SubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ['id', 'result_url', 'nick_name', 'duplicate']
