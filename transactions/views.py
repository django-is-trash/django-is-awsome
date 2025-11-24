from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Transaction
from .serializers import TransactionSerializer
from .filters import TransactionFilter


class TransactionListCreateView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['transaction_at', 'amount']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        account = serializer.validated_data["account"]

        if account.user != self.request.user:
            raise PermissionDenied("이 계좌에 거래를 생성할 수 없습니다.")

        amount = serializer.validated_data["amount"]
        type = serializer.validated_data["type"]

        # balance 계산
        if type == "INCOME":
            new_balance = account.balance + amount
        else:
            new_balance = account.balance - amount

        transaction = serializer.save(
            user=self.request.user,
            balance_after=new_balance
        )

        account.balance = new_balance
        account.save()


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)