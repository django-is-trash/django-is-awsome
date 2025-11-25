from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm



@login_required
def transaction_html_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "transactions/transaction_list.html", {
        "transactions": transactions,
    })

@login_required
def transaction_create_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("transactions:transaction_html")
    else:
        form = TransactionForm(user=request.user)

    return render(request, "transactions/transaction_form.html", {"form": form})

@login_required
def transaction_detail_view(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user,
    )
    return render(
        request,
        "transactions/transaction_detail.html",
        {"transaction": transaction},
    )

@login_required
def transaction_update_view(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user,  # 내 거래만
    )

    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user, instance=transaction)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.user = request.user
            tx.save()
            return redirect("transactions:transaction_detail", pk=tx.pk)
    else:
        form = TransactionForm(user=request.user, instance=transaction)

    return render(
        request,
        "transactions/transaction_form.html",
        {
            "form": form,
            "is_edit": True, #템플릿 구분
            "transaction": transaction,
        },
    )

@login_required
def transaction_delete_view(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        transaction.delete()
        return redirect("transactions:transaction_html")