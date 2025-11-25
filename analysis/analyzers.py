import matplotlib
matplotlib.use("Agg")

import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings


class Analyzer:
    def __init__(self, user, about, period_type, start_date, end_date, description="", graph_type="CATEGORY"):
        self.user = user
        self.about = about
        self.period_type = period_type
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.graph_type = graph_type

        # 사용자별 폴더 생성
        self.output_dir = os.path.join(settings.MEDIA_ROOT, "analysis", str(user.id))
        os.makedirs(self.output_dir, exist_ok=True)

    def get_transactions(self):
        from transactions.models import Transaction

        qs = Transaction.objects.filter(
            user=self.user,
            transacted_at__date__gte=self.start_date,
            transacted_at__date__lte=self.end_date,
        ).values("transacted_at", "amount", "type", "category")

        return pd.DataFrame(qs)

    def build_dataframe(self):
        df = self.get_transactions()

        if df.empty:
            return df

        df["transacted_at"] = pd.to_datetime(df["transacted_at"])
        return df

    # 수입/지출/차액 계산
    def calculate_totals(self, df):
        total_income = df[df["type"] == "deposit"]["amount"].sum()
        total_spending = df[df["type"] == "withdraw"]["amount"].sum()
        difference = total_income - total_spending
        return total_income, total_spending, difference

    # 수입 vs 지출 비교 그래프
    def build_plot(self, total_income, total_spending):
        plt.figure(figsize=(6, 4))

        labels = ["Income", "Spending"]
        values = [total_income, total_spending]

        colors = ["#4CAF50", "#EF5350"]

        plt.bar(labels, values, color=colors)
        plt.title("Income vs Spending")
        plt.ylabel("Amount")
        plt.tight_layout()

    # 카테고리별 지출 그래프
    def build_category_plot(self, df):
        plt.figure(figsize=(6, 6))

        # 지출 데이터만 추출
        spending_df = df[df["type"] == "withdraw"]

        if spending_df.empty:
            raise ValueError("해당 기간에는 지출 데이터가 없어 카테고리 그래프를 생성할 수 없습니다.")

        # 카테고리별 합계
        category_sum = spending_df.groupby("category")["amount"].sum()

        category_colors = [
            "#4DB6AC", "#9575CD", "#FF8A65",
            "#4FC3F7", "#FFF176", "#81C784"
        ]

        plt.pie(
            category_sum,
            labels=category_sum.index,
            autopct="%1.1f%%",
            colors=category_colors[:len(category_sum)],
            startangle=90,
        )
        plt.title("Spending by Category")
        plt.tight_layout()

    def save_plot_as_image(self):
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join(self.output_dir, filename)

        plt.savefig(filepath)
        plt.close()

        return f"analysis/{self.user.id}/{filename}"

    # 모델 저장 (수입/지출/차액)
    def save_analysis_model(self, image_path, total_income, total_spending, difference):
        from .models import Analysis
        analysis = Analysis.objects.create(
            user=self.user,
            about=self.about,
            type=self.period_type,
            period_start=self.start_date,
            period_end=self.end_date,
            description=self.description,
            result_image=image_path,

            total_income=total_income,
            total_spending=total_spending,
            difference=difference,
        )
        return analysis

    def run(self):
        df = self.build_dataframe()
        if df.empty:
            raise ValueError("해당 기간에 분석 가능한 거래가 없습니다.")

        # 수입/지출/차액
        total_income, total_spending, difference = self.calculate_totals(df)

        # 그래프 생성
        if self.graph_type == "TOTAL":
            self.build_plot(total_income, total_spending)
        else:
            self.build_category_plot(df)

        image_path = self.save_plot_as_image()

        return self.save_analysis_model(image_path, total_income, total_spending, difference)
