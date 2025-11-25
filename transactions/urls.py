from django.urls import path

from .views import TransactionListCreateView, TransactionDetailView

from .views_html import transaction_html_view, transaction_create_view, transaction_detail_view, transaction_update_view, transaction_delete_view

app_name = 'transactions'

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction_list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),


#     html 연결 > 기존거 그냥 두고 밑에 추가했어요
    path("html/", transaction_html_view, name="transaction_html"),
    path("html/create/", transaction_create_view, name="transaction_create"),
    path('html/<int:pk>/', transaction_detail_view, name='transaction_detail_html'), # 이름중복 수정
    path('html/<int:pk>/update/', transaction_update_view, name='transaction_update'),
    path("html/<int:pk>/delete/", transaction_delete_view, name="transaction_delete_html"),


]