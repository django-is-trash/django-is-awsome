from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from transactions.models import Transaction

from django.db.models import Sum
from datetime import date

@login_required
def home(request):
    user = request.user

    # 최근 거래 10개
    recent_transactions = (
        Transaction.objects
        .filter(user=user)
        .select_related("account")
        .order_by("-transacted_at")[:10]
    )

    today = date.today()
    month_start = date(today.year, today.month, 1)

    month_transactions = Transaction.objects.filter(
        user=user,
        transacted_at__date__gte=month_start
    )

    month_income = month_transactions.filter(type="deposit").aggregate(total=Sum("amount"))["total"] or 0
    month_spending = month_transactions.filter(type="withdraw").aggregate(total=Sum("amount"))["total"] or 0
    month_diff = month_income - month_spending

    context = {
        "recent_transactions": recent_transactions,
        "month_income": month_income,
        "month_spending": month_spending,
        "month_diff": month_diff,
    }

    return render(request, "main.html", context)

