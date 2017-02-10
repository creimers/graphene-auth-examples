from django.contrib.auth import get_user_model
import pytest
from rest_framework_jwt.serializers import JSONWebTokenSerializer

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def user():
    user = User(email="eins@zwei.de")
    user.set_password('123')
    user.save()
    return user


@pytest.fixture
@pytest.mark.django_db
def token(user):
    serializer = JSONWebTokenSerializer(
        data={'email': user.email, 'password': '123'})
    serializer.is_valid()
    token = serializer.object['token']
    return token
