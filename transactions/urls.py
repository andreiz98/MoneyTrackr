from transactions import views
from django.urls import path

urlpatterns = [
    path('addTransaction/', views.add_transactions,name='add_transaction'),
    path('allTransactions/', views.all_transactions,name='all_transactions'),
]