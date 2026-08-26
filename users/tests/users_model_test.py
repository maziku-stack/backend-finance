import pytest
from users.users_models import CustomUser

@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(
        email='user@example.com',
        first_name='Test',
        last_name='User',
        phone='1234567890',
        password='Password123!'
    )
    assert user.email == 'user@example.com'
    assert user.is_active
    assert not user.is_staff
    assert user.check_password('Password123!')

@pytest.mark.django_db
def test_create_superuser():
    admin = CustomUser.objects.create_superuser(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        phone='0987654321',
        password='AdminPass123!'
    )
    assert admin.email == 'admin@example.com'
    assert admin.is_active
    assert admin.is_staff
    assert admin.is_superuser
