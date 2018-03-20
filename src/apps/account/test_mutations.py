import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser.email import ActivationEmail, PasswordResetEmail

from djoser import utils

from config.schema import schema
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
            email: "affe@giraffe.de",
            password: "123",
            passwordRepeat: "123"
        )
      {
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
        email: "affe@giraffe.de",
        password: "123",
        passwordRepeat: "1234"
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
        email: "affe@giraffe.de",
        password: "123",
        passwordRepeat: "123"
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
    email_factory = ActivationEmail(
        request, {'user': user})
    context = email_factory.get_context_data()
    token = context.get('token')
    uid = context.get('uid')

    query = """
    mutation {
        activate(
            token: "%s",
            uid: "%s",
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

    user.refresh_from_db()
    assert user.is_active is True

    # TODO: test error case


# ########
# LOGIN
# ########

@pytest.mark.django_db
def test_login_mutation_success(user, rf):
    request = rf.request()
    query = """
    mutation {
        login(
            email: "eins@zwei.de",
            password: "123"
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
    assert result.data['login']['errors'] is None
    assert type(result.data['login']['token']) == str


@pytest.mark.django_db
def test_login_mutation_error(rf):
    request = rf.request()
    query = """
    mutation {
        login(
            email: "eins@zwei.de",
            password: "123"
        ) {
            success
            errors
            token
        }
    }
    """

    result = schema.execute(query, context_value=request)
    assert result.data['login']['errors'] is not None
    assert result.data['login']['token'] is None
    assert result.data['login']['success'] is False


# ##############
# REAUTHENTICATE
# ##############
@pytest.mark.django_db
def test_refresh_token_success(client, token):
    """
    successfully refresh JWT
    """
    query = """
    mutation {
        refreshToken(
            token: "%s",
        ) {
            success
            errors
            token
        }
    }
    """ % token.split(' ')[1]
    query = "/graphql?query=%s" % query
    response = client.post(query, HTTP_AUTHORIZATION=token)
    result = response.json()
    assert type(result['data']['refreshToken']['token']) is str

# ##############
# PASSWORD RESET
# ##############
@pytest.mark.django_db
def test_reset_password_success(client):
    """
    successfully request a password reset
    """
    query = """
    mutation {
        resetPassword(
            email: "eins@zwei.de"
        ) {
            success
        }
    }
    """
    query = "/graphql?query=%s" % query
    response = client.post(query)
    result = response.json()
    assert type(result['data']['resetPassword']['success'])

# ######################
# PASSWORD RESET CONFIRM
# ######################
@pytest.mark.django_db
def test_reset_password_confirm_success(client, user):
    """
    successfully confirm a password reset
    """

    uid = utils.encode_uid(user.pk)
    token = default_token_generator.make_token(user)

    query = """
    mutation {
        resetPasswordConfirm(
            email: "eins@zwei.de"
            uid: "%s"
            token: "%s"
            newPassword: "666"
            reNewPassword: "666"
        ) {
            success
        }
    }
    """ % (uid, token)
    query = "/graphql?query=%s" % query
    response = client.post(query)
    result = response.json()
    assert type(result['data']['resetPasswordConfirm']['success'])


@pytest.mark.django_db
def test_reset_password_confirm_password_error(client, user):
    """
    confirm password reset error password missmatch
    """

    uid = utils.encode_uid(user.pk)
    token = default_token_generator.make_token(user)

    query = """
    mutation {
        resetPasswordConfirm(
            email: "eins@zwei.de"
            uid: "%s"
            token: "%s"
            newPassword: "666"
            reNewPassword: "6667"
        ) {
            success
        }
    }
    """ % (uid, token)
    query = "/graphql?query=%s" % query
    response = client.post(query)
    result = response.json()
    assert not result['data']['resetPasswordConfirm']['success']


@pytest.mark.django_db
def test_reset_password_confirm_token_error(client, user):
    """
    confirm password reset token error
    """

    uid = utils.encode_uid(user.pk)
    token = "Angela Merkel"

    query = """
    mutation {
        resetPasswordConfirm(
            email: "eins@zwei.de"
            uid: "%s"
            token: "%s"
            newPassword: "666"
            reNewPassword: "666"
        ) {
            success
        }
    }
    """ % (uid, token)
    query = "/graphql?query=%s" % query
    response = client.post(query)
    result = response.json()
    assert not result['data']['resetPasswordConfirm']['success']


@pytest.mark.django_db
def test_reset_password_confirm_uid_error(client, user):
    """
    confirm password reset uid error
    """

    uid = "Angela Merkel"
    token = default_token_generator.make_token(user)

    query = """
    mutation {
        resetPasswordConfirm(
            email: "eins@zwei.de"
            uid: "%s"
            token: "%s"
            newPassword: "666"
            reNewPassword: "666"
        ) {
            success
        }
    }
    """ % (uid, token)
    query = "/graphql?query=%s" % query
    response = client.post(query)
    result = response.json()
    assert not result['data']['resetPasswordConfirm']['success']

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
            email: "eins@zwei.de",
            password: "123"
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
            email: "wrong@user.de",
            password: "123"
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
            email: "eins@zwei.de",
            password: "wrong_password"
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
            email: "eins@zwei.de",
            password: "123"
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
