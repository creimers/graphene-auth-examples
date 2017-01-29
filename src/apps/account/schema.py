from graphene import relay, AbstractType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import User as UserModel


class User(DjangoObjectType):
    """
    how does this work?
    """
    class Meta:
        model = UserModel
        filter_fields = {
            'id': ['exact', ]
            }
        exclude_fields = ('password', )
        interfaces = (relay.Node, )


class UserQuery(AbstractType):
    """
    how does this work?
    """
    user = relay.Node.Field(User)
    users = DjangoFilterConnectionField(User)
