import pytest

from django.core import mail

from test_fixtures.users import user
from .utils import send_activation_email, send_password_reset_email


@pytest.mark.django_db
def test_send_activtion_email(user, rf):
    request = rf.request()
    send_activation_email(user, request)
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_send_password_reset_email(user, rf):
    request = rf.request()
    send_password_reset_email(user, request)
    assert len(mail.outbox) == 1
