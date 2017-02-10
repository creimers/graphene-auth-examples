from config.schema import schema
from django.contrib.auth import get_user_model
from djoser import utils
import pytest
from test_fixtures.users import token, user


User = get_user_model()


# ########
# REGISTER
# ########

@pytest.mark.django_db
def test_register_mutation_success(rf):
    request = rf.request()
    query = """
    mutation {
      register(
        input: {
            email: "affe@giraffe.de",
            password: "123",
            passwordRepeat: "123"
        }
      ) {
        success
        errors
      }
    }
    """

    expectation = {
            'register': {
                'success': True,
                'errors': None
                }
            }
    result = schema.execute(query, context_value=request)
    assert not result.errors
    assert result.data == expectation


@pytest.mark.django_db
def test_register_mutation_password_error(rf):
    request = rf.request()
    query = """
    mutation {
      register(
        input: {
            email: "affe@giraffe.de",
            password: "123",
            passwordRepeat: "1234"
        }
      ) {
        success
        errors
      }
    }
    """

    expectation = {
            'register': {
                'success': False,
                'errors': ['password', "Passwords don't match."]
                }
            }
    result = schema.execute(query, context_value=request)
    assert not result.errors
    assert result.data == expectation


@pytest.mark.django_db
def test_register_mutation_user_error(rf):
    request = rf.request()
    query = """
    mutation {
      register(
        input: {
            email: "affe@giraffe.de",
            password: "123",
            passwordRepeat: "123"
        }
      ) {
        success
        errors
      }
    }
    """

    expectation = {
            'register': {
                'success': False,
                'errors': ['email', 'Email already registered.']
                }
            }
    schema.execute(query)
    second_result = schema.execute(query, context_value=request)
    assert not second_result.errors
    assert second_result.data == expectation


# ########
# ACTIVATE
# ########

@pytest.mark.django_db
def test_activation_success(user, rf):
    request = rf.request()
    user.is_active = False
    user.save()
    email_factory = utils.UserActivationEmailFactory.from_request(
        request, user=user)
    context = email_factory.get_context()
    token = context.get('token')
    uid = context.get('uid')

    query = """
    mutation {
        activate(
            input: {
                token: "%s",
                uid: "%s",
            }
        ) {
            success
            errors
        }
    }
    """ % (token, uid)

    expectation = {
            'activate': {
                'success': True,
                'errors': None
                }
            }

    result = schema.execute(query, context_value=request)
    assert not result.errors
    assert result.data == expectation


# ########
# LOGIN
# ########

@pytest.mark.django_db
def test_login_mutation_success(user, rf):
    request = rf.request()
    query = """
    mutation {
        login(
            input: {
                email: "eins@zwei.de",
                password: "123"
            }
        ) {
            success
            errors
            token
            user {
                email
            }
        }
    }
    """

    result = schema.execute(query, context_value=request)
    assert not result.errors
    assert type(result.data['login']['token']) == str


@pytest.mark.django_db
def test_login_mutation_error(rf):
    request = rf.request()
    query = """
    mutation {
        login(
            input: {
                email: "eins@zwei.de",
                password: "123"
            }
        ) {
            success
            errors
            token
        }
    }
    """

    result = schema.execute(query, context_value=request)
    assert not result.errors
    assert result.data['login']['token'] is None
    assert result.data['login']['success'] is False


# ##############
# REAUTHENTICATE
# ##############

# ##############
# PASSWORD RESET
# ##############

# ################
# SET NEW PASSWORD
# ################

# ################
# PROFILE UPDATE
# ################

# ################
# DELETE ACCOUNT
# ################
@pytest.mark.django_db
def test_delete_account_unauthenticated_error(client):
    """
    error because unauthenticated
    """
    query = """
    mutation {
        deleteAccount(
            input: {
                email: "eins@zwei.de",
                password: "123"
            }
        ) {
            success
            errors
        }
    }
    """
    query = "/graphql?query=%s" % query
    response = client.post(query)
    result = response.json()
    assert response.status_code == 200
    assert not result['data']['deleteAccount']['success']


@pytest.mark.django_db
def test_delete_account_authenticated_user_error(client, token):
    """
    error because authenticated as wrong user
    """
    query = """
    mutation {
        deleteAccount(
            input: {
                email: "wrong@user.de",
                password: "123"
            }
        ) {
            success
            errors
        }
    }
    """
    query = "/graphql?query=%s" % query
    response = client.post(query, HTTP_AUTHORIZATION=token)
    result = response.json()
    assert response.status_code == 200
    assert not result['data']['deleteAccount']['success']


@pytest.mark.django_db
def test_delete_account_authenticated_password_error(client, token):
    """
    error because authenticated user provides wrong password
    """
    query = """
    mutation {
        deleteAccount(
            input: {
                email: "eins@zwei.de",
                password: "wrong_password"
            }
        ) {
            success
            errors
        }
    }
    """
    query = "/graphql?query=%s" % query
    response = client.post(query, HTTP_AUTHORIZATION=token)
    result = response.json()
    assert response.status_code == 200
    assert not result['data']['deleteAccount']['success']
    assert result['data']['deleteAccount']['errors'] == ['wrong password']


@pytest.mark.django_db
def test_delete_account_authenticated_success(client, token, user):
    """
    authenticated user can successfully delete their account
    """
    query = """
    mutation {
        deleteAccount(
            input: {
                email: "eins@zwei.de",
                password: "123"
            }
        ) {
            success
            errors
        }
    }
    """
    query = "/graphql?query=%s" % query
    response = client.post(query, HTTP_AUTHORIZATION=token)
    result = response.json()
    assert response.status_code == 200
    assert result['data']['deleteAccount']['success']
    assert not User.objects.filter(email=user.email).count()
