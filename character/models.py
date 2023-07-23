from django.db import models
from question.models import Question, Poll
from accounts.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class Submit(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    result_url = models.TextField(null=True)
    nick_name = models.CharField(max_length=200, null=True)


class Answer(BaseModel):
    submit_id = models.ForeignKey(Submit, on_delete=models.CASCADE, null=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    num = models.IntegerField(null=False)
    content = models.CharField(max_length=200, null=True)
