from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    # 추가 필드를 여기에 정의
    # 예를 들면, 닉네임(nickname)을 저장하는 필드를 추가
    # nickname = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'
