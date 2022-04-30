from rest_framework.serializers import ModelSerializer, Serializer, CharField, ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User, UnicodeUsernameValidator
from noxcrux_api.models.UserKeysContainer import UserKeysContainer
from django.contrib.auth.password_validation import validate_password


class UserSerializer(Serializer):
    class Meta:
        fields = ['username', 'password', 'public_key', 'protected_key', 'iv']

    username = CharField(max_length=128, required=True, validators=[UnicodeUsernameValidator(), UniqueValidator(queryset=User.objects.all(), message="A user with that username already exists.")])
    password = CharField(max_length=128, write_only=True, required=True)
    public_key = CharField(required=True)
    protected_key = CharField(required=True)
    iv = CharField(required=True)

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as error:
            raise ValidationError({'password': error})
        return value

    def save(self, **kwargs):
        user = User.objects.create_user(username=self.validated_data['username'], password=self.validated_data['password'])
        UserKeysContainer.objects.filter(user=user).update(public_key=self.validated_data['public_key'], protected_key=self.validated_data['protected_key'], iv=self.validated_data['iv'])
        return UserKeysContainer.objects.get(user=user)


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class PasswordUpdateSerializer(Serializer):

    old_password = CharField(max_length=128, write_only=True, required=True)
    new_password1 = CharField(max_length=128, write_only=True, required=True)
    new_password2 = CharField(max_length=128, write_only=True, required=True)
    protected_key = CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('Password incorrect')
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise ValidationError({'new_password2': "Passwords didn't match."})
        validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        UserKeysContainer.objects.filter(user=user).update(protected_key=self.validated_data['protected_key'])
        return user
