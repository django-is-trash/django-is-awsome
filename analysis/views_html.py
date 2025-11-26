from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .analyzers import Analyzer
from .models import Analysis

from .utils import (
    get_daily_range, get_last_day_range,
    get_week_range, get_last_week_range,
    get_month_range, get_last_month_range,
    get_year_range, get_last_year_range,
)

@login_required
def analysis_list_html(request):
    user = request.user
    period = request.GET.get("period")  # URL 파라미터 받아오기

    qs = Analysis.objects.filter(user=user).order_by("-created_at")

    # period 조건 적용
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

    return render(request, "analysis/analysis_list.html", {
        "analyses": qs
    })

@login_required
def analysis_create_html(request):
    result = None
    error = None

    if request.method == "POST":
        analysis_type = request.POST.get("type")
        graph_type = request.POST.get("graph_type", "CATEGORY")

        # 기간 계산
        mapping = {
            "DAILY": get_daily_range,
            "LAST_DAY": get_last_day_range,
            "WEEKLY": get_week_range,
            "LAST_WEEK": get_last_week_range,
            "MONTHLY": get_month_range,
            "LAST_MONTH": get_last_month_range,
            "YEARLY": get_year_range,
            "LAST_YEAR": get_last_year_range,
        }

        if analysis_type not in mapping:
            return render(
                request,
                "analysis/analysis_create.html",
                {"error": "유효하지 않은 타입"}
            )

        start, end = mapping[analysis_type]()

        analyzer = Analyzer(
            user=request.user,
            about="TOTAL_SPENDING",
            period_type=analysis_type,
            start_date=start,
            end_date=end,
            description="",
            graph_type=graph_type,
        )

        try:
            result = analyzer.run()
        except ValueError as e:
            error = str(e)

    return render(request, "analysis/analysis_create.html", {
        "result": result,
        "error": error,
    })



