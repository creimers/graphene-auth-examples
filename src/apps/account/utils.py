from djoser.compat import get_user_email, get_user_email_field_name
from djoser.email import ActivationEmail, PasswordResetEmail


def send_activation_email(user, request):
    to = [get_user_email(user)]
    ActivationEmail(request, {'user': user}).send(to)


def send_password_reset_email(user, request):
    to = [get_user_email(user)]
    PasswordResetEmail(request, {'user': user}).send(to)
