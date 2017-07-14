from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser.serializers import UidAndTokenSerializer, PasswordRetypeSerializer
from djoser import utils
from rest_framework import serializers

User = get_user_model()


class UidAndTokenSerializer(UidAndTokenSerializer):

    def validate_uid(self, value):
        try:
            uid = utils.decode_uid(value)
            self.user = User.objects.get(pk=uid)
        except (
                User.DoesNotExist,
                ValueError,
                TypeError,
                OverflowError
                ) as error:
            raise serializers.ValidationError(
                self.error_messages['invalid_uid'])
        return value

    def validate(self, attrs):
        self.validate_uid(attrs['uid'])
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError(
                self.error_messages['invalid_token'])
        return attrs


class PasswordResetConfirmRetypeSerializer(
        UidAndTokenSerializer, PasswordRetypeSerializer
        ):
    def validate(self, attrs):
        attrs = super(PasswordResetConfirmRetypeSerializer, self)\
            .validate(attrs)
        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError(
                self.error_messages['password_mismatch'])
        return attrs
