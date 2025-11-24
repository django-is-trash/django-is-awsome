from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id','name', 'created_at',
        ]
        read_only_fields = ['created_at']