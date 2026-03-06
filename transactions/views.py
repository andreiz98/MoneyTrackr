import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from transactions.models import Transaction


# Create your views here.

@login_required
def add_transactions(request):
    transact = Transaction.objects.filter(user=request.user)

    income = sum(t.amount for t in transact if t.type == 'income')
    expenses = sum(t.amount for t in transact if t.type == 'expense')
    balance = income - expenses

    if request.method == "POST":
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        type_ = request.POST.get('type')

        if title and amount and type_:
            Transaction.objects.create(
                user=request.user,
                title=title,
                amount=amount,
                type=type_
            )
            return redirect('add_transaction')

    context = {
        'transactions': transact,
        'income': income,
        'expenses': expenses,
        'balance': balance,
    }

    return render(request, "transactions/add_transactions.html", context)

@login_required()
def all_transactions(request):
    search_query = request.GET.get('q', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    type_filter = request.GET.get('type', '')
    min_amount = request.GET.get('min_amount', '')
    max_amount = request.GET.get('max_amount', '')

    transactions = Transaction.objects.filter(user=request.user)

    if request.GET:
        if search_query:
            transactions = transactions.filter(title__icontains=search_query)
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        if type_filter in ['income', 'expense']:
            transactions = transactions.filter(type=type_filter)
        if min_amount:
            transactions = transactions.filter(amount__gte=min_amount)
        if max_amount:
            transactions = transactions.filter(amount__lte=max_amount)

    context = {
        'transactions': transactions.order_by('-date'),
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'min_amount': min_amount,
        'max_amount': max_amount,
        'type_filter': type_filter,
    }

    return render(request, "transactions/all_transactions.html", context)
