from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Account
from .forms import AccountForm


@login_required
def account_list_view(request):
    accounts = Account.objects.filter(user=request.user).order_by("created_at")
    return render(request, "accounts/account_list.html", {
        "accounts": accounts,
    })


@login_required
def account_create_view(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("accounts:account_list")
    else:
        form = AccountForm()
    return render(request, "accounts/account_form.html", {
        "form": form,
    })


@login_required
def account_delete_view(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)

    if request.method == "POST":
        account.delete()
        return redirect("accounts:account_list")

    return redirect("accounts:account_list")
