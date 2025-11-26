from django.db import models
from django.conf import settings

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('INCOME', '수입'),
        ('EXPENSE', '지출'),
    ]

    CATEGORY_CHOICES = [
        ('식비', '식비'),
        ('카페/간식', '카페/간식'),
        ('교통/차량', '교통/차량'),
        ('쇼핑/패션', '쇼핑/패션'),
        ('마트/편의점', '마트/편의점'),
        ('주거/통신', '주거/통신'),
        ('의료/건강', '의료/건강'),
        ('문화/여가', '문화/여가'),
        ('여행/숙박', '여행/숙박'),
        ('교육/학습', '교육/학습'),
        ('경조사/선물', '경조사/선물'),
        ('급여', '급여'),
        ('용돈', '용돈'),
        ('금융이자', '금융이자'),
        ('기타', '기타'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



    transaction_at = models.DateField(verbose_name="거래일")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='EXPENSE', verbose_name="구분")
    amount = models.IntegerField(verbose_name="금액")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='식비', verbose_name="카테고리")
    memo = models.CharField(max_length=100, blank=True, verbose_name="메모")



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transaction_at'] # 최신순 정렬

    def __str__(self):
        return f"{self.memo} ({self.amount})"
