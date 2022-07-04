from rest_framework.serializers import ModelSerializer, SlugRelatedField, CharField, CurrentUserDefault
from noxcrux_api.models.UserKeysContainer import UserKeysContainer


class UserPublicKeySerializer(ModelSerializer):
    class Meta:
        model = UserKeysContainer
        fields = ['user', 'public_key']

    user = SlugRelatedField(slug_field='username', read_only=True, default=CurrentUserDefault())
    public_key = CharField(read_only=True)
