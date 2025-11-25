from django.db import models
from django.contrib.auth import get_user_model
from accounts.constants import ANALYSIS_TYPES, ANALYSIS_ABOUT

User = get_user_model()


class Analysis(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,related_name="analyses",verbose_name="사용자"
    )

    # 어떤 것을 분석한 것인지 (총 지출, 총 수입 등)
    about = models.CharField(
        max_length=30,choices=ANALYSIS_ABOUT,verbose_name="분석 대상"
    )

    # 어떤 기간으로 분석했는지 (매주, 매월, 매년)
    type = models.CharField(
        max_length=20,choices=ANALYSIS_TYPES,verbose_name="분석 단위"
    )

    # 분석 기간
    period_start = models.DateField(verbose_name="분석 시작일")
    period_end = models.DateField(verbose_name="분석 종료일")

    # 분석 설명
    description = models.TextField(
        blank=True,verbose_name="분석 설명"
    )

    # 시각화된 그래프 이미지 저장
    result_image = models.ImageField(
        upload_to="analysis/",blank=True,null=True,verbose_name="결과 그래프"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,verbose_name="생성일"
    )
    updated_at = models.DateTimeField(
        auto_now=True,verbose_name="수정일"
    )

    # 수익 / 지출 / 차이
    total_income = models.IntegerField(default=0, verbose_name="총 수입")
    total_spending = models.IntegerField(default=0, verbose_name="총 지출")
    difference = models.IntegerField(default=0, verbose_name="차액")

    def __str__(self):
        return f"{self.user.username} - {self.get_about_display()} ({self.get_type_display()})"
