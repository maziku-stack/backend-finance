import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.users_models import CustomUser
from finance.finance_models import Category
from datetime import date

@pytest.mark.django_db
def test_get_categories():
    client = APIClient()
    user = CustomUser.objects.create_user(
        email='test@example.com',
        first_name='Test',
        last_name='User',
        phone='1234567890',
        password='testpass123'
    )
    client.force_authenticate(user=user)

    Category.objects.create(name='Food', icon='fa-utensils')
    Category.objects.create(name='Transport', icon='fa-bus')

    url = reverse('category-list')  # Default router auto-names this
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_create_transaction():
    client = APIClient()
    user = CustomUser.objects.create_user(
        email='creator@example.com',
        first_name='Creator',
        last_name='User',
        phone='0987654321',
        password='creator123'
    )
    client.force_authenticate(user=user)

    category = Category.objects.create(name='Dining')

    url = reverse('transaction-list')

    data = {
        'date': date.today().isoformat(),
        'description': 'Dinner out',
        'category_id': category.id,
        'amount': '35.50',
        'is_income': False,
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['description'] == 'Dinner out'
    assert response.data['amount'] == '35.50'

@pytest.mark.django_db
def test_transaction_requires_auth():
    client = APIClient()
    url = reverse('transaction-list')
    response = client.get(url)
    assert response.status_code == 401  # Unauthorized without login
