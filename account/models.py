from django.db import models
from django.conf import settings

class Transaction(models.Model):

    TYPE_CHOICES = [
        ('INCOME', '수입'),
        ('EXPENSE', '지출'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    transaction_at = models.DateField(verbose_name="거래일")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='EXPENSE', verbose_name="구분")
    amount = models.IntegerField(verbose_name="금액")
    category = models.CharField(max_length=50, verbose_name="카테고리")
    memo = models.CharField(max_length=100, blank=True, verbose_name="메모")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_at']
                    '   def __str__(self):
        return f"{self.memo} ({self.amount})"