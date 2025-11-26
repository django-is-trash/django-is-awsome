from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
    path('update/<int:pk>/', views.transaction_list, name='transaction_update'),
]