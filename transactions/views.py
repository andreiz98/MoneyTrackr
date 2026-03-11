from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from transactions.forms import ExpenseForm, IncomeForm
from transactions.models import Transaction


# Create your views here.

class AddIncome(LoginRequiredMixin, CreateView):
    template_name = 'transactions/add_income.html'
    model = Transaction
    form_class = IncomeForm
    success_url = '/addIncome/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.type = f'income'
        return super().form_valid(form)

class AddExpenses(LoginRequiredMixin, CreateView):
    template_name = 'transactions/add_expenses.html'
    form_class = ExpenseForm
    model = Transaction
    success_url = '/addExpenses/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.type = f'expense'
        return super().form_valid(form)

class TransactionDetailView(LoginRequiredMixin, ListView):
    template_name = 'transactions/all_transactions.html'
    model = Transaction
    context_object_name = 'all_transaction'

    def get_context_data(self, **kwargs):

        search_query = self.request.GET.get('q', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        type_filter = self.request.GET.get('type', '')
        min_amount = self.request.GET.get('min_amount', '')
        max_amount = self.request.GET.get('max_amount', '')

        transactions = Transaction.objects.filter(user=self.request.user)

        if self.request.method == "GET":
            if search_query:
                transactions = transactions.filter(title__icontains=search_query)
            if start_date:
                transactions = transactions.filter(date__gte=start_date)
            if end_date:
                transactions = transactions.filter(date__lte=end_date)
            if type_filter in ['income', 'food', 'transport','rent',
            'utilities','entertainment','shopping','health', 'education','subscriptions','other']:
                transactions = transactions.filter(type=type_filter)
            if min_amount:
                transactions = transactions.filter(amount__gte=min_amount)
            if max_amount:
                transactions = transactions.filter(amount__lte=max_amount)

        context = {
            'all_transaction': transactions.order_by('-date'),
            'start_date': start_date,
            'end_date': end_date,
            'min_amount': min_amount,
            'max_amount': max_amount,
            'type_filter': type_filter,
        }

        return context