import pytest

from rest_framework_jwt.serializers import JSONWebTokenSerializer

from test_fixtures.users import user


@pytest.mark.django_db
def test_unauthenticated_user(client):
    query = "/graphql?query={viewer{id, email}}"
    response = client.post(query)
    assert response.status_code == 200
    result = response.json()
    assert result['data']['viewer'] is None


@pytest.mark.django_db
def test_authenticated_user(user, client):
    serializer = JSONWebTokenSerializer(
        data={'email': user.email, 'password': '123'})
    serializer.is_valid()
    token = serializer.object['token']

    query = "/graphql?query={viewer{id, email}}"
    response = client.post(query, HTTP_AUTHORIZATION="JWT %s" % token)
    assert response.status_code == 200
    result = response.json()
    assert result['data']['viewer']['email'] == user.email
