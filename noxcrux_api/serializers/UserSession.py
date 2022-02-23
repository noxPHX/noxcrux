from rest_framework.serializers import ModelSerializer, SlugRelatedField, CurrentUserDefault
from noxcrux_api.models.UserSession import UserSession
from rest_framework.authtoken.models import Token


class UserTokenSerializer(ModelSerializer):

    class Meta:
        model = Token
        fields = ['created']


class UserSessionSerializer(ModelSerializer):

    user = SlugRelatedField(slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        model = UserSession
        fields = '__all__'
