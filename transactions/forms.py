from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_at', 'type', 'category', 'amount', 'memo']
        widgets = {
            'transaction_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 식비'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '금액'}),
            'memo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '내용'}),
        }