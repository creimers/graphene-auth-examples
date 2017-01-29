import pytest

from config.schema import schema
from test_fixtures.users import user


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
