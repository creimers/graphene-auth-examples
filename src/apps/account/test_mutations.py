import pytest

from ...config.schema import schema


@pytest.mark.django_db
def test_register_mutation_success():
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
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expectation


@pytest.mark.django_db
def test_register_mutation_password_error():
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
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expectation


@pytest.mark.django_db
def test_register_mutation_user_error():
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
    second_result = schema.execute(query)
    assert not second_result.errors
    assert second_result.data == expectation
