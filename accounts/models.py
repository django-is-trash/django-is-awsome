from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)

    balance = models.IntegerField(default=0) # 현재 잔액 표기

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"