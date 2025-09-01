import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from user.serializers import UserSerializer, AuthTokenSerializer


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def user_data():
    return {"email": "test@example.com", "password": "password123"}


@pytest.mark.django_db
def test_user_serializer_create(user_data):
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])


@pytest.mark.django_db
def test_user_serializer_update(user_data):
    User = get_user_model()
    user = User.objects.create_user(**user_data)
    data = {"first_name": "John", "last_name": "Doe", "password": "newpass123"}
    serializer = UserSerializer(instance=user, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save()
    assert updated.first_name == "John"
    assert updated.last_name == "Doe"
    assert updated.check_password("newpass123")


@pytest.mark.django_db
def test_user_serializer_invalid():
    data = {"email": "bad-email", "password": "123"}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "email" in serializer.errors or "password" in serializer.errors


@pytest.mark.django_db
def test_auth_token_serializer_valid(user_data, factory):
    User = get_user_model()
    user = User.objects.create_user(**user_data)
    request = factory.post("/")
    serializer = AuthTokenSerializer(
        data={"email": user_data["email"], "password": user_data["password"]},
        context={"request": request}
    )
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["user"] == user


@pytest.mark.django_db
def test_auth_token_serializer_invalid_password(user_data, factory):
    User = get_user_model()
    User.objects.create_user(**user_data)
    request = factory.post("/")
    serializer = AuthTokenSerializer(
        data={"email": user_data["email"], "password": "wrongpass"},
        context={"request": request}
    )
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors or "authorization" in serializer.errors


@pytest.mark.django_db
def test_auth_token_serializer_missing_fields(factory):
    request = factory.post("/")
    serializer = AuthTokenSerializer(data={"password": "pass123"}, context={"request": request})
    assert not serializer.is_valid()
    assert "email" in serializer.errors

    serializer = AuthTokenSerializer(data={"email": "a@test.com"}, context={"request": request})
    assert not serializer.is_valid()
    assert "password" in serializer.errors
