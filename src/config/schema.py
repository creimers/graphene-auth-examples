import graphene

from apps.account.mutations import (
    Activate,
    DeleteAccount,
    Login,
    RefreshToken,
    Register,
    )
from apps.account.schema import User
from graphene_django.filter import DjangoFilterConnectionField


class RootQuery(graphene.ObjectType):
    viewer = graphene.Field(User)
    node = graphene.relay.Node.Field()
    users = DjangoFilterConnectionField(User)

    def resolve_viewer(self, args, context, info):
        if context.user.is_authenticated():
            return context.user
        return None


class Mutation(graphene.ObjectType):
    activate = Activate.Field()
    login = Login.Field()
    register = Register.Field()
    deleteAccount = DeleteAccount.Field()
    refreshToken = RefreshToken.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutation)
