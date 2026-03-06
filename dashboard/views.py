from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from transactions.models import Transaction


# Create your views here.

@login_required
def dashboard(request):
    search_query = request.GET.get('q', '')
    transactions = Transaction.objects.filter(user=request.user)

    if search_query:
        transactions = transactions.filter(title__icontains=search_query)

    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expenses

    context = {
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'search_query': search_query,
    }

    return render(request, "homepage/dashboard.html", context)