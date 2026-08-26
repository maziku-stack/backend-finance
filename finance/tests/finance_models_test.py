import pytest
from finance.finance_models import Category,Transaction,SavingsGoal,MonthlySummary
from users.users_models import CustomUser
from datetime import date

@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name="Food", icon="fa-utensils")
    assert category.name == "Food"

@pytest.mark.django_db
def test_create_transaction():
    user = CustomUser.objects.create_user(
        email="jumane@gmail.com",
        first_name="Jumane",
        last_name="Henry",
        phone="07017654321",
        password="i_love_coding@1"
    )
    category = Category.objects.create(name="Transport", icon="fa-bus")
    transaction = Transaction.objects.create(
        user=user,
        date=date.today(),
        description="Bus fare",
        category=category,
        amount=2.50,
        is_income=False
    )
    assert transaction.description == "Bus fare"
    assert transaction.user.email == "busfare@gmail.com"

@pytest.mark.django_db
def test_savings_goal_progress():
    user = CustomUser.objects.create_user("henryjumamane1@gmail.com", "Jummane", "Henry", "0765123456", "jumahenry")
    goal = SavingsGoal.objects.create(
        user=user,
        name="Emergency Fund",
        target_amount=1000,
        current_amount=200,
    )
    assert goal.progress_percent() == 20

@pytest.mark.django_db
def test_monthly_summary_unique_constraint():
    user = CustomUser.objects.create_user("immanuelmaziku@gmail.com", "Immanuel", "Maziku", "0781143866", "love_you_momy@1")
    summary1 = MonthlySummary.objects.create(
        user=user,
        month=date(2026, 8, 24),
        total_income=1000000,
        total_expenses=300000,
        amount_saved=700000,
    )
    with pytest.raises(Exception):
        MonthlySummary.objects.create(
            user=user,
            month=date(2026, 8, 23),
            total_income=1000000,
            total_expenses=250000,
            amount_saved=750000,
        )
