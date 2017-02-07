from graphene import relay, AbstractType, String, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import User as UserModel


class User(DjangoObjectType):
    """
    User Node
    """
    class Meta:
        model = UserModel
        filter_fields = {
            'email': ['exact', ]
            }
        exclude_fields = ('password', )
        interfaces = (relay.Node, )

    is_logged_in = Boolean()

    def resolve_is_logged_in(self, args, context, info):
        return context.user.is_authenticated()


class UserQuery(AbstractType):
    """
    how does this work?
    """
    user = relay.Node.Field(User)
    users = DjangoFilterConnectionField(User)
