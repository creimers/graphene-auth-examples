import graphene
from graphene import relay

from .models import User


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
                user = User.objects.create(email=email, password=password)
                return Register(success=bool(user.id))
            except:
                errors = ["email", "Email already registered."]
                return Register(success=False, errors=errors)
        errors = ["password", "Passwords don't match."]
        return Register(success=False, errors=errors)
