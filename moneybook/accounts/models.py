from django.db import models
from django.contrib.auth import get_user_model
from .constants import BANK_CODES, ACCOUNT_TYPE

User = get_user_model()


class Account(models.Model):
    user = models.ForeignKey(
        User,on_delete=models.CASCADE,related_name="accounts",
    )

    bank_code = models.CharField(
        max_length=3,choices=BANK_CODES, verbose_name="은행",
    )

    account_number = models.CharField(
        max_length=30,verbose_name="계좌번호",
    )

    account_type = models.CharField(
        max_length=30,choices=ACCOUNT_TYPE,verbose_name="계좌 종류",
    )

    name = models.CharField(
        max_length=50,verbose_name="계좌/지갑 이름",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,verbose_name="생성일",
    )

    def __str__(self):
        return f"[{self.name}]{self.get_bank_code_display()} - {self.get_account_type_display()}"
