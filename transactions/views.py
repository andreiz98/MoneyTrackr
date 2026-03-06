from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from transactions.models import Transaction


# Create your views here.

@login_required
def add_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)
    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
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
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance
    }

    return render(request, "transactions/add_transactions.html", context)

@login_required()
def all_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)

    context = {
        'transactions': transactions,
    }

    return render(request, "transactions/all_transactions.html", context)
