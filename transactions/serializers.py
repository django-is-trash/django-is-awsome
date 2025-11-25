from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'account','user' ,'amount', 'category', 'memo',
            'transacted_at', 'created_at', 'updated_at', 'type'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']