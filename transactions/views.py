from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import openpyxl
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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
            if start_date and end_date:
                transactions = transactions.filter(date__date__range=[start_date, end_date])
            else:
                now = timezone.now()
                transactions = transactions.filter(date__year=now.year, date__month=now.month)
            if type_filter in ['income', 'food', 'transport', 'rent',
                               'utilities', 'entertainment', 'shopping', 'health', 'education', 'subscriptions',
                               'other']:
                transactions = transactions.filter(type=type_filter)
            if min_amount:
                transactions = transactions.filter(amount__gte=min_amount)
            if max_amount:
                transactions = transactions.filter(amount__lte=max_amount)

        context = {
            'all_transaction': transactions.order_by('-date'),
            'start_date': start_date or '',
            'end_date': end_date or '',
            'min_amount': min_amount,
            'max_amount': max_amount,
            'type_filter': type_filter,
        }

        return context

@login_required
def export_excel(request):
    transactions = Transaction.objects.filter(user=request.user)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=transactions.xlsx'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Transactions'

    worksheet.append([
        'Title',
        'Amount',
        'Category',
        'Date'
    ])

    for t in transactions:
        worksheet.append([
            t.title,
            float(t.amount),
            t.category.name if t.category else '',
            t.date.strftime("%Y-%m-%d")
        ])

    workbook.save(response)

    return response


@login_required
def export_pdf(request):
    transactions = Transaction.objects.filter(user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    data = [['Title', 'Amount', 'Category', 'Type', 'Date']]

    for t in transactions:
        data.append([
            t.title,
            f"{t.amount} RON",
            t.category.name if t.category else 'N/A',
            t.type,
            t.date.strftime("%d/%m/%Y %H:%M")
        ])

    table = Table(data, colWidths=[120, 80, 100, 80, 120])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ])
    table.setStyle(style)

    elements.append(table)
    doc.build(elements)

    return response