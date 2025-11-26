from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm

@login_required(login_url='/admin/login/')
def transaction_list(request):
    # [1] 생성 로직 (POST 요청 시)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user # 로그인 사용자 자동 연결
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    # [2] 조회 및 필터링 로직 (GET 요청 시)
    # 로그인한 사용자의 데이터만 가져옵니다.
    transactions = Transaction.objects.filter(user=request.user)

    search_type = request.GET.get('search_type')
    search_query = request.GET.get('search_query')

    if search_type:
        transactions = transactions.filter(type=search_type)

    if search_query:
        # memo 필드 검색
        transactions = transactions.filter(memo__icontains=search_query)

    # [3] 상단 요약 카드 계산 (전체 데이터 기준)
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
    }


    return render(request, 'transactions/transaction_list.html', context)

@login_required
def transaction_delete(request, pk):

    if request.method == 'POST':

        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transaction.delete()
    return redirect('transaction_list')