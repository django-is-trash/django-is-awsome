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
        account = serializer.validated_data['account']

        if account.user != self.request.user:
            raise PermissionDenied("이 계좌에 거래를 생성할 수 없습니다.")

        # 계좌의 최신 balance_after = 최근 거래 balance_after
        last_transaction = (
            account.transactions.order_by('-transaction_at', '-id').first()
        )

        last_balance = last_transaction.balance_after if last_transaction else 0

        amount = serializer.validated_data['amount']
        type = serializer.validated_data['type']

        # 새 잔액 계산
        if type == 'INCOME':
            new_balance = last_balance + amount
        else:
            new_balance = last_balance - amount

        # 저장
        serializer.save(
            user=self.request.user,
            balance_after=new_balance
        )

def recalc_account_transactions(account):
    transactions = account.transactions.order_by('transaction_at', 'id')

    balance = 0
    for tx in transactions:
        if tx.type == "INCOME":
            balance += tx.amount
        else:
            balance -= tx.amount

        tx.balance_after = balance
        tx.save()

class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    # 거래 삭제 후 전체 재계산
    def perform_destroy(self, instance):
        account = instance.account
        instance.delete()

        recalc_account_transactions(account)

    # 거래 수정 후 전체 재계산
    def perform_update(self, serializer):
        instance = self.get_object()
        account = instance.account

        serializer.save()

        recalc_account_transactions(account)