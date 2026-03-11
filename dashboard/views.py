import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from transactions.models import Transaction


# Create your views here.

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income - expense

    data = (transactions.filter(type='expense')
            .values('category__name', 'category__color')
            .annotate(total=Sum('amount')))

    labels = ['Income'] + [x['category__name'] for x in data]
    amounts = [float(income)] + [float(x['total']) for x in data]
    colors = ['#198754'] + [x['category__color'] for x in data]

    context = {
        "transactions": transactions[:5],  # recent transactions
        "income": income,
        "expenses": expense,
        "balance": balance,
        "labels": json.dumps(labels),
        "amounts": json.dumps(amounts),
        "colors": json.dumps(colors),
    }

    return render(request, "homepage/dashboard.html", context)