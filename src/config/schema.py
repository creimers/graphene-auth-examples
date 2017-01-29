import graphene

from apps.account.mutations import Activate, Login, Register
from apps.account.schema import UserQuery


class Query(
        UserQuery,
        graphene.ObjectType
        ):
    pass


class Mutation(graphene.ObjectType):
    activate = Activate.Field()
    login = Login.Field()
    register = Register.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
