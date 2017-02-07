import graphene

from apps.account.mutations import Activate, Login, Register
from apps.account.schema import User
#  from apps.account.schema import UserQuery


class RootQuery(graphene.ObjectType):
    viewer = graphene.Field(User)

    def resolve_viewer(self, args, context, info):
        if context.user.is_authenticated():
            return context.user
        return None


class Mutation(graphene.ObjectType):
    activate = Activate.Field()
    login = Login.Field()
    register = Register.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutation)
