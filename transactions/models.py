from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Account

User = get_user_model()

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('INCOME', '입금'),
        ('EXPENSE', '출금'),
    ]

    CATEGORY_CHOICES = [
        ('food', '식비'),
        ('transport', '교통'),
        ('shopping', '쇼핑'),
        ('income', '수입'),
        ('etc', '기타'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.IntegerField()
    balance_after = models.IntegerField()

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    memo = models.CharField(max_length=255, blank=True)

    transaction_at = models.DateField()   # ERD 기준 필드명

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_at']
