from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Analysis
from .serializers import AnalysisSerializer
from .analyzers import Analyzer
from .utils import (
    get_daily_range,
    get_last_day_range,
    get_week_range,
    get_last_week_range,
    get_month_range,
    get_last_month_range,
    get_year_range,
    get_last_year_range,
)


# 조회 (ListAPIView)
class AnalysisListView(ListAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Analysis.objects.filter(user=user).order_by("-created_at")

        period = self.request.query_params.get("period")

        if period == "DAILY":
            start, end = get_daily_range()
            qs = qs.filter(period_start=start, period_end=end)

        elif period == "LAST_DAY":
            start, end = get_last_day_range()
            qs = qs.filter(period_start=start, period_end=end)

        elif period == "WEEKLY":
            start, end = get_week_range()
            qs = qs.filter(period_start=start, period_end=end)

        elif period == "LAST_WEEK":
            start, end = get_last_week_range()
            qs = qs.filter(period_start=start, period_end=end)

        elif period == "MONTHLY":
            start, end = get_month_range()
            qs = qs.filter(period_start=start, period_end=end)

        elif period == "LAST_MONTH":
            start, end = get_last_month_range()
            qs = qs.filter(period_start=start, period_end=end)

        elif period == "YEARLY":
            start, end = get_year_range()
            qs = qs.filter(period_start=start, period_end=end)

        elif period == "LAST_YEAR":
            start, end = get_last_year_range()
            qs = qs.filter(period_start=start, period_end=end)

        return qs


# 생성 (APIView)
class AnalysisCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        analysis_type = request.data.get("type")
        about = request.data.get("about", "TOTAL_SPENDING")
        description = request.data.get("description", "")

        # 기간 계산
        if analysis_type == "DAILY":
            start_date, end_date = get_daily_range()
        elif analysis_type == "LAST_DAY":
            start_date, end_date = get_last_day_range()
        elif analysis_type == "WEEKLY":
            start_date, end_date = get_week_range()
        elif analysis_type == "LAST_WEEK":
            start_date, end_date = get_last_week_range()
        elif analysis_type == "MONTHLY":
            start_date, end_date = get_month_range()
        elif analysis_type == "LAST_MONTH":
            start_date, end_date = get_last_month_range()
        elif analysis_type == "YEARLY":
            start_date, end_date = get_year_range()
        elif analysis_type == "LAST_YEAR":
            start_date, end_date = get_last_year_range()
        else:
            return Response({"error": "Invalid type"}, status=400)

        analyzer = Analyzer(
            user=user,
            about=about,
            period_type=analysis_type,
            start_date=start_date,
            end_date=end_date,
            description=description,
        )

        result = analyzer.run()

        return Response({
            "id": result.id,
            "type": result.type,
            "about": result.about,
            "period_start": result.period_start,
            "period_end": result.period_end,
            "image_url": result.result_image.url if result.result_image else None,
        })
