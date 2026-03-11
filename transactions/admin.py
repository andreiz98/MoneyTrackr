from django.contrib import admin

from transactions.models import Category, Transaction


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'type', 'category', 'user', 'date')
    list_filter = ('type', 'category', 'user')
