from django.urls import path

from .views import TransactionListCreateView, TransactionDetailView

app_name = 'transactions'

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction_list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
]
