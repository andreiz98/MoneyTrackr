from transactions import views
from django.urls import path

urlpatterns = [
    path('allTransactions/', views.TransactionDetailView.as_view(),name='all_transactions'),
    path('addExpenses/', views.AddExpenses.as_view(),name='add_expenses'),
    path('addIncome/', views.AddIncome.as_view(),name='add_income'),
    path('exportExcel/', views.export_excel,name='export_excel'),
    path('export-pdf/', views.export_pdf, name="export_pdf"),
]