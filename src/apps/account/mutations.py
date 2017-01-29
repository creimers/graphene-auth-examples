import graphene
from graphene import relay

from .models import User


class Register(relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_repeat = graphene.String(required=True)

    success = graphene.Boolean()

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
                pass
        return Register(success=False)
