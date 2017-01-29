from djoser import settings as djoser_settings

import graphene
from graphene import relay

from rest_framework_jwt.serializers import JSONWebTokenSerializer

from .models import User
from .utils import send_activation_email


class Register(relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_repeat = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        email = input.get('email')
        password = input.get('password')
        password_repeat = input.get('password_repeat')

        if password == password_repeat:
            try:
                user = User.objects.create(
                    email=email,
                    password=password,
                    is_active=False
                    )
                if djoser_settings.get('SEND_ACTIVATION_EMAIL'):
                    send_activation_email(user, context)
                return Register(success=bool(user.id))
            except:
                errors = ["email", "Email already registered."]
                return Register(success=False, errors=errors)
        errors = ["password", "Passwords don't match."]
        return Register(success=False, errors=errors)


class Login(relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        serializer = JSONWebTokenSerializer(data=input)
        if serializer.is_valid():
            token = serializer.object['token']
            return Login(success=True, token=token, errors=None)
        else:
            return Login(
                success=False,
                token=None,
                errors=['email', 'Unable to login with provided credentials.']
                )
