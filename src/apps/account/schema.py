from graphene import relay, AbstractType, ObjectType, Field
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
        exclude_fields = ('password', 'is_superuser', )
        interfaces = (relay.Node, )


class UserQuery(AbstractType):
    """
    what is an abstract type?
    http://docs.graphene-python.org/en/latest/types/abstracttypes/
    """
    user = relay.Node.Field(User)
    users = DjangoFilterConnectionField(User)


class Viewer(ObjectType):
    user = Field(User)

    def resolve_user(self, args, context, info):
        if context.user.is_authenticated():
            return context.user
        return None
