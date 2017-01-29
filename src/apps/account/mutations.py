import graphene
from graphene import relay

from .models import User


class Register(relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_repeat = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        email = input.get('email')
        password = input.get('password')
        password_repeat = input.get('password_repeat')

        if password == password_repeat:
            try:
                user = User.objects.create(email=email, password=password)
                return Register(ok=bool(user.id))
            except Exception as e:
                pass
        return Register(ok=False)
