from transactions.models import Transaction

def get_balance(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user)
        income = sum(t.amount for t in transactions if t.type == 'income')
        expenses = sum(t.amount for t in transactions if t.type == 'expense')
        balance = income - expenses
    else:
        balance = 0
    return {'balance': balance}