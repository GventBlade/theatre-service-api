import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from user.serializers import UserSerializer, AuthTokenSerializer


@pytest.fixture
def user_data():
    return {"email": "test@example.com", "password": "password123"}


@pytest.fixture
def request_context():
    factory = APIRequestFactory()
    request = factory.post("/")
    return {"request": request}


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
    data = {"first_name": "New", "last_name": "Surname"}
    serializer = UserSerializer(instance=user, data=data, partial=True)
    assert serializer.is_valid()
    updated = serializer.save()
    assert updated.first_name == "New"
    assert updated.last_name == "Surname"


@pytest.mark.django_db
def test_user_serializer_invalid():
    data = {"email": "bad-email", "password": "123"}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "email" in serializer.errors
    assert "password" in serializer.errors


@pytest.mark.django_db
def test_auth_token_serializer_missing_email(request_context):
    serializer = AuthTokenSerializer(
        data={"password": "somepass"}, context=request_context
    )
    assert not serializer.is_valid()
    assert "email" in serializer.errors


@pytest.mark.django_db
def test_auth_token_serializer_invalid_password(user_data, request_context):
    User = get_user_model()
    User.objects.create_user(**user_data)
    bad = {"email": user_data["email"], "password": "wrongpass"}
    serializer = AuthTokenSerializer(data=bad, context=request_context)
    assert not serializer.is_valid()
    assert (
        "non_field_errors" in serializer.errors
        or "non_field_errors" in serializer.errors.keys()
    )


@pytest.mark.django_db
def test_auth_token_serializer_missing_email(request_context):
    serializer = AuthTokenSerializer(
        data={"password": "somepass"}, context=request_context
    )
    assert not serializer.is_valid()
    assert "email" in serializer.errors
