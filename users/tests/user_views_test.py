import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.users_models import CustomUser

@pytest.mark.django_db
def test_user_list_requires_auth():
    client = APIClient()
    url = reverse("users-list")
    response = client.get(url)
    assert response.status_code == 401  # Unauthorized if not logged in

@pytest.mark.django_db
def test_user_list_as_admin():
    client = APIClient()
    admin_user = CustomUser.objects.create_superuser(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        phone="123",
        password="adminpass"
    )
    client.force_authenticate(admin_user)
    url = reverse("users-list")
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_create_user_via_api():
    client = APIClient()
    admin_user = CustomUser.objects.create_superuser(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        phone="123",
        password="adminpass"
    )
    client.force_authenticate(admin_user)

    url = reverse("users-list")
    payload = {
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "phone": "4567890",
        "password": "NewPass123!",
        "password2": "NewPass123!"
    }
    response = client.post(url, payload, format='json')
    assert response.status_code == 201
    assert response.data['email'] == payload['email']

@pytest.mark.django_db
def test_create_user_password_mismatch_api():
    client = APIClient()
    admin_user = CustomUser.objects.create_superuser(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        phone="123",
        password="adminpass"
    )
    client.force_authenticate(admin_user)

    url = reverse("users-list")
    payload = {
        "email": "badpass@example.com",
        "first_name": "Bad",
        "last_name": "User",
        "phone": "0000000",
        "password": "pass1",
        "password2": "pass2"
    }
    response = client.post(url, payload, format='json')
    assert response.status_code == 400
    assert "password" in response.data
