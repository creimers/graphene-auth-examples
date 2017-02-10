from djoser import utils


def send_activation_email(user, request):
    email_factory = utils.UserActivationEmailFactory.from_request(
        request, user=user)
    email = email_factory.create()
    email.send()


def send_password_reset_email(user, request):
    email_factory = utils.UserPasswordResetEmailFactory.from_request(
        request, user=user)
    email = email_factory.create()
    email.send()
