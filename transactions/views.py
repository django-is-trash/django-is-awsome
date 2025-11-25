from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import PermissionDenied
from .filters import TransactionFilter

class TransactionListCreateView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ['category']  # /?category=food
    filterset_class = TransactionFilter
    ordering_fields = ['transacted_at', 'amount']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     qs = Transaction.objects.filter(user=user)
    #
    #     start = self.request.query_params.get("start")
    #     end = self.request.query_params.get("end")
    #
    #     if start:
    #         qs = qs.filter(transacted_at__gte=start)
    #     if end:
    #         qs = qs.filter(transacted_at__lte=end)
    #     return qs

    def perform_create(self, serializer):
        account_user = serializer.validated_data['accounts']
        if account_user != self.request.user:
            raise PermissionDenied("이 계좌에 거래를 생성할 수 없습니다.")
        serializer.save(user=self.request.user)


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

@login_required
def transaction_list_view(request):
    transactions = (
        Transaction.objects
        .filter(user=request.user)
        .order_by('-created_at')
    )
    return render(request, "transactions/transaction_list.html", {
        "transactions": transactions,
    })
