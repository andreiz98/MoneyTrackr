from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from transactions.models import Transaction


# Create your views here.

@login_required
def dashboard(request):
    transactions = Transaction.objects.all()

    income = sum(t.amount for t in transactions if t.type == 'income')

    expenses = sum(t.amount for t in transactions if t.type == 'expense')

    balance = income - expenses

    context = {
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance
    }

    return render(request, "homepage/dashboard.html", context)