from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "deposit", "입금"
        WITHDRAW = "withdraw", "출금"

    CATEGORY_CHOICES = [
        ("food", "식비"),
        ("transport", "교통"),
        ("shopping", "쇼핑"),
        ("income", "수입"),
        ("etc", "기타"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="사용자",
    )

    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="계좌",
    )

    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        default=TransactionType.WITHDRAW,
        verbose_name="거래 유형",
    )

    amount = models.IntegerField(verbose_name="거래 금액")  # 항상 양수로입력받도록
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="카테고리")
    memo = models.CharField(max_length=255, blank=True, verbose_name="메모")

    transacted_at = models.DateTimeField(verbose_name="거래 시각")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-transacted_at"]

    def __str__(self):
        return f"{self.account} / {self.amount}"
