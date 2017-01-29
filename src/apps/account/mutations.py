from django.contrib.auth.tokens import default_token_generator

from djoser import settings as djoser_settings
from djoser.utils import decode_uid

import graphene
from graphene import relay

from rest_framework_jwt.serializers import JSONWebTokenSerializer

from .models import User
from .utils import send_activation_email


class Register(relay.ClientIDMutation):
    """
    Mutation to register a user
    """
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


class Activate(relay.ClientIDMutation):
    """
    Mutation to activate a user's registration
    """
    class Input:
        token = graphene.String(required=True)
        uid = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        token = input.get('token')
        uid = input.get('uid')

        try:
            uid = decode_uid(uid)
            user = User.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                return Activate(success=False, errors=['stale token'])
                pass
            return Activate(success=True, errors=None)

        except:
            return Activate(success=False, errors=['unknown user'])


class Login(relay.ClientIDMutation):
    """
    Mutation to login a user
    """
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    token = graphene.String()
    # TODO: should return user object!

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
