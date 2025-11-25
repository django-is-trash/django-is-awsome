from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["bank_code", "account_number", "account_type", "name"]
        widgets = {
            "bank_code": forms.Select(),
            "account_type": forms.Select(),
            "account_number": forms.TextInput(attrs={"placeholder": "계좌번호"}),
            "name": forms.TextInput(attrs={"placeholder": "계좌별명"})
        }
