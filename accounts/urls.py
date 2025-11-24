from django.urls import path
from .views import AccountListCreateView, AccountDetailView

app_name = 'accounts'

urlpatterns = [
    path('', AccountListCreateView.as_view(), name='account_list'),
    path('<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
]
