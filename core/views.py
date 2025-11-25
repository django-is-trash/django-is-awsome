from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Account
from transactions.models import Transaction

@login_required
def home(request):
    user = request.user

    # 유저 정보
    profile = user

    # 최근 거래
    recent_transactions = (
        Transaction.objects
        .filter(user=user)
        .select_related("account")
        .order_by("-transacted_at")[:10]
    )

    context = {
        "profile": profile,
        "recent_transactions": recent_transactions,
    }
    return render(request, "main.html", context)