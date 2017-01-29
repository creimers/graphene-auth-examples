import graphene

from apps.account.mutations import Register
from apps.account.schema import UserQuery


class Query(
        UserQuery,
        graphene.ObjectType
        ):
    pass


class Mutation(graphene.ObjectType):
    register = Register.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
