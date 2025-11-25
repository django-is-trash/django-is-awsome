
from django.http import HttpResponse
from analysis.analyzers import Analyzer
from datetime import date

def test_analysis(request):
    analyzer = Analyzer(
        user=request.user,
        about="TOTAL_SPENDING",
        period_type="MONTHLY",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
        description="테스트 분석"
    )
    result = analyzer.run()
    return HttpResponse(f"생성된 분석 ID: {result.id}, 이미지={result.result_image.url}")
