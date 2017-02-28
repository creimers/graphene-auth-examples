from test_fixtures.users import user, token
import pytest


@pytest.mark.django_db
def test_unauthenticated_user(client):
    query = "/graphql?query={viewer{user{id, email}}}"
    response = client.post(query)
    assert response.status_code == 200
    result = response.json()
    assert result['data']['viewer'] is None


@pytest.mark.django_db
def test_authenticated_user(user, token, client):
    query = "/graphql?query={viewer{user{id, email}}}"
    response = client.post(query, HTTP_AUTHORIZATION=token)
    assert response.status_code == 200
    result = response.json()
    assert result['data']['viewer']['user']['email'] == user.email
