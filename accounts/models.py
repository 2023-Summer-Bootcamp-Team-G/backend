from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, user_id):
        return self.get(user_id=user_id)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=200, primary_key=True)
    nick_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

    def get_by_natural_key(self, user_id):
        return self.get(user_id=user_id)

    def __str__(self):
        return self.user_id


# table에 last_login, is_superuser 속성이 생기는데 이걸 제거하려고 시도했는데
# 제거하려면 Django의 인증 시스템에서 사용되는 기능을 직접 구현하고
# 이건 되게 복잡하고 권장하지 않다고 해서 일단 이렇게 구현은 했어

# login Post를 보낼 때 `Manager' object has no attribute 'get_by_natural_key` 이오류가 발생했음
