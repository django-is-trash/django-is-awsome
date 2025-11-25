from django import forms
from .models import Transaction
from accounts.models import Account


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["account","type", "amount", "category", "memo", "transacted_at"]

        widgets = {
            "type": forms.RadioSelect,
            "transacted_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "memo": forms.TextInput(attrs={"placeholder": "메모를 입력하세요"}),
            "amount": forms.NumberInput(attrs={"placeholder": "금액 (예: 5000)"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["account"].queryset = Account.objects.filter(user=user)
