from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=200, primary_key=True)
    nick_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.id

# table에 last_login, is_superuser 속성이 생기는데 이걸 제거하려고 시도했는데
# 제거하려면 Django의 인증 시스템에서 사용되는 기능을 직접 구현하고
# 이건 되게 복잡하고 권장하지 않다고 해서 일단 이렇게 구현은 했어