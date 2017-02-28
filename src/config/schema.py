import graphene

from apps.account.mutations import (
    Activate,
    DeleteAccount,
    Login,
    RefreshToken,
    Register,
    ResetPassword,
    ResetPasswordConfirm,
    )
from apps.account.schema import User, Viewer


class RootQuery(graphene.ObjectType):
    viewer = graphene.Field(Viewer)
    node = graphene.relay.Node.Field()

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
    resetPassword = ResetPassword.Field()
    resetPasswordConfirm = ResetPasswordConfirm.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutation)
