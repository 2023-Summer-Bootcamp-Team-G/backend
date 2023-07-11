from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class Poll(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Question(BaseModel):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE, null=False)
    question_number = models.IntegerField(null=False)
    question_text = models.CharField(max_length=200, null=False)
