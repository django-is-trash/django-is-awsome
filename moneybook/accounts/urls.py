from django.urls import path
from . import views  # views 모듈 전체를 불러오기

app_name = "accounts"

urlpatterns = [
    path("", views.account_list_view, name="account_list"),
    path("create/", views.account_create_view, name="account_create"),
    path("<int:pk>/delete/", views.account_delete_view, name="account_delete"),
]
