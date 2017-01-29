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
        ok
      }
    }
    """
    result = schema.execute(query)
    assert not result.errors
    assert result.data['register']['ok']
