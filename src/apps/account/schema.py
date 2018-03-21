from graphene import relay, ObjectType, Field
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField

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


class UserQuery(object):
    """
    what is an abstract type?
    http://docs.graphene-python.org/en/latest/types/abstracttypes/
    """
    user = relay.Node.Field(User)
    users = DjangoFilterConnectionField(User)


class Viewer(ObjectType):
    user = Field(User)

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
