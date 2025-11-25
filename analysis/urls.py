from django.urls import path
from .views import AnalysisListView, AnalysisCreateView
from .views_html import analysis_list_html, analysis_create_html

app_name = "analysis"

urlpatterns = [
    # API
    path("api/", AnalysisListView.as_view(), name="analysis_list"),
    path("api/create/", AnalysisCreateView.as_view(), name="analysis_create"),

    # HTML
    path("html/", analysis_list_html, name="analysis_html"),
    path("html/create/", analysis_create_html, name="analysis_create_html"),
]
