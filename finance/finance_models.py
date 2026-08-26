from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} ({'Income' if self.is_income else 'Expense'})"

class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def progress_percent(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    def __str__(self):
        return self.name

class MonthlySummary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='monthly_summaries')
    month = models.DateField()  # store the first day of the month as reference
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_saved = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ('user', 'month')

    def __str__(self):
        return f"{self.user.email} - {self.month.strftime('%B %Y')}"
