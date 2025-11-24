from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user', 'name', 'balance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'balance', 'created_at', 'updated_at']
