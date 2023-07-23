from django.db import models
from models import BaseModel
from accounts.models import User


class Poll(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Question(BaseModel):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE, null=False)
    question_number = models.IntegerField(null=False)
    question_text = models.CharField(max_length=200, null=False)
