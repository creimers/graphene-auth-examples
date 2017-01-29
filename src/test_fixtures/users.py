import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db
def user():
    user = User(email="eins@zwei.de")
    user.set_password('123')
    user.save()
    return user
