from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', '수입'),
        ('OUT', '지출'),
    ]

    date = models.DateField(default=timezone.now, verbose_name="날짜")
    amount = models.PositiveIntegerField(verbose_name="금액")
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES, default='OUT', verbose_name="구분")
    description = models.CharField(max_length=100, blank=True, verbose_name="내용")

    def __str__(self):
        return f"{self.date} - {self.amount} ({self.get_type_display()})"

    class Meta:
        ordering = ['-date', '-id']