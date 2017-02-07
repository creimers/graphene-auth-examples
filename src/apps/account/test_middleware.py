import pytest

from rest_framework_jwt.serializers import JSONWebTokenSerializer

from config.schema import schema
from test_fixtures.users import user


@pytest.mark.django_db
def test_request_user(user, client):
    serializer = JSONWebTokenSerializer(
        data={'email': user.email, 'password': '123'})
    serializer.is_valid()
    token = serializer.object['token']

    query = "/graphql?query={users{edges{node{id, email, isLoggedIn}}}}"
    response = client.post(query, HTTP_AUTHORIZATION="JWT %s" % token)
    assert response.status_code == 200
    print(response.json())
