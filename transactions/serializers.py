from rest_framework import serializers
from .models import Transaction
from accounts.models import Account

class TransactionSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source='account'
    )

    class Meta:
        model = Transaction
        fields = [
            'id','user','account_id',
            'type','amount','balance_after','category',
            'memo','transaction_at','created_at','updated_at',
        ]
        read_only_fields = ['user', 'balance_after', 'created_at', 'updated_at']
