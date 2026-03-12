from django import forms

from transactions.models import Transaction


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'category', 'date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Description'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        get_amount = cleaned_data.get('amount')
        if get_amount <= 0:
            self.add_error('amount', 'Amount must be greater than 0')

        return cleaned_data

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short Description'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data

        get_amount = cleaned_data.get('amount')
        if get_amount <= 0:
            self.add_error('amount', 'Amount must be greater than 0')

        return cleaned_data