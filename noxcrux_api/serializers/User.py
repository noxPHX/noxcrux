from rest_framework.serializers import ModelSerializer, Serializer, CharField, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from noxcrux_api.models.Generator import Generator


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password=validated_data['password'])
        Generator.objects.create(owner=user)
        return user


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class PasswordUpdateSerializer(Serializer):

    old_password = CharField(max_length=128, write_only=True, required=True)
    new_password1 = CharField(max_length=128, write_only=True, required=True)
    new_password2 = CharField(max_length=128, write_only=True, required=True)

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
        return user
