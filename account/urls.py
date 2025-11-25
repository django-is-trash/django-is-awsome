from django.urls import path
from . import views

urlpatterns = [
    # 메인 페이지 (여기서 조회, 생성, 필터링 모두 처리)
    path('', views.transaction_list, name='transaction_list'),

    # 삭제 처리 (화면 없이 로직만 수행하고 메인으로 돌아옴)
    path('delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
]