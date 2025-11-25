from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # id / username / email / password 는 AbstractUser 에 포함
    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^01[0-9]{8,9}$')],
        verbose_name="전화번호",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="계정 생성 시각",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="정보 수정 시각",
    )

    def __str__(self):
        return self.username
