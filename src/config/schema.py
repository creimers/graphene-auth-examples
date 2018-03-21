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

    def resolve_viewer(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
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
