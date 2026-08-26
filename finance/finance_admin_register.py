from django.contrib import admin
from .finance_models import Category,Transaction,SavingsGoal,MonthlySummary

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'category', 'amount', 'is_income', 'date')
    list_filter = ('is_income', 'category', 'date')
    search_fields = ('description',)

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'target_amount', 'current_amount')
    search_fields = ('name', 'user__email')

@admin.register(MonthlySummary)
class MonthlySummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'total_income', 'total_expenses', 'amount_saved')
    list_filter = ('month',)
    search_fields = ('user__email',)
