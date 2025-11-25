from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm

def transaction_list(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    transactions = Transaction.objects.all()
    search_type = request.GET.get('search_type')
    search_query = request.GET.get('search_query')

    if search_type:
        transactions = transactions.filter(type=search_type)
    if search_query:
        transactions = transactions.filter(description__icontains=search_query)

    context = {'transactions': transactions, 'form': form}
    return render(request, 'transaction_list.html', context)

def transaction_delete(request, pk):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.delete()
    return redirect('transaction_list')