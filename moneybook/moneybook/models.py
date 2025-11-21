from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Moneybook(models.Model):
    CATEGORY_CHOICES = (
        ('shop', '쇼핑'),
        ('travel', '여행'),
        ('food', '식비'),
        ('medic', '의료비'),
        ('ect','기타')
    )

    category = models.CharField('카테고리', max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField('메모', max_length=100)
    content = models.IntegerField('금액')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created = models.DateTimeField('작성일자', auto_now_add=True)
    updated = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title[:10]}"


class Meta:
    verbose_name = '가계부'
    verbose_name_plural = '결제 내역'