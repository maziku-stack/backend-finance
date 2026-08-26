import pytest
from finance.finance_serializer import CategorySerializer,TransactionSerializer,SavingsGoalSerializer
from finance.finance_models import Category
from datetime import date
from decimal import Decimal

@pytest.mark.django_db
def test_category_serializer():
    category = Category(name='Food', icon='fa-utensils')
    serializer = CategorySerializer(category)
    assert serializer.data['name'] == 'Food'

@pytest.mark.django_db
def test_transaction_serializer_valid_data():
    category = Category.objects.create(name='Transport')
    data = {
        'date': date.today(),
        'description': 'Train ticket',
        'category': {'name': 'Transport', 'icon': 'fa-bus'},
        'amount': '12.50',
        'is_income': False,
    }
    serializer = TransactionSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    transaction = serializer.save()
    assert transaction.description == 'Train ticket'
    assert transaction.category.name == 'Transport'

@pytest.mark.django_db
def test_transaction_serializer_invalid_missing_date():
    data = {
        'description': 'Bus ticket',
        'category': {'name': 'Transport', 'icon': 'fa-bus'},
        'amount': '5.00',
        'is_income': False,
    }
    serializer = TransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'date' in serializer.errors

@pytest.mark.django_db
def test_savings_goal_serializer():
    data = {
        'name': 'Emergency Fund',
        'target_amount': '1000',
        'current_amount': '200',
    }
    serializer = SavingsGoalSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    savings_goal = serializer.save()
    progress = savings_goal.progress_percent()
    assert progress == 20
