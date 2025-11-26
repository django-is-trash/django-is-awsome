from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm

@login_required(login_url='/admin/login/')
def transaction_list(request, pk=None):

    if pk:
        target_transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    else:
        target_transaction = None


    if request.method == 'POST':

        form = TransactionForm(request.POST, instance=target_transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')


    else:

        form = TransactionForm(instance=target_transaction)


    transactions = Transaction.objects.filter(user=request.user)


    search_type = request.GET.get('search_type')
    search_query = request.GET.get('search_query')
    if search_type:
        transactions = transactions.filter(type=search_type)
    if search_query:
        transactions = transactions.filter(memo__icontains=search_query)


    my_data = Transaction.objects.filter(user=request.user)
    total_income = my_data.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = my_data.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    context = {
        'transactions': transactions,
        'form': form,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'update_pk': pk,
    }

    return render(request, 'transactions/transaction_list.html', context)

@login_required
def transaction_delete(request, pk):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transaction.delete()
    return redirect('transaction_list')