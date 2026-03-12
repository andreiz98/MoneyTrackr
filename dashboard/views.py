import json
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import ListView

from transactions.models import Transaction


# Create your views here.

class DashboardView(LoginRequiredMixin, ListView):
    template_name = "homepage/dashboard.html"
    model = Transaction
    context_object_name = "transactions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            transactions = Transaction.objects.filter(user=user, date__date__range=[start, end])
        else:
            transactions = Transaction.objects.filter(user=user, date__year=now.year, date__month=now.month)

        income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income - expense

        data = (transactions.filter(type='expense')
                .values('category__name', 'category__color')
                .annotate(total=Sum('amount')))

        labels = ['Income'] + [x['category__name'] for x in data]
        amounts = [float(income)] + [float(x['total']) for x in data]
        colors = ['#198754'] + [x['category__color'] for x in data]

        context.update({
            "transactions": transactions.order_by('-date')[:5],
            "income": income,
            "expenses": expense,
            "balance": balance,
            "labels": json.dumps(labels),
            "amounts": json.dumps(amounts),
            "colors": json.dumps(colors),
            "start_date": start_date or '',
            "end_date": end_date or ''
        })

        return context