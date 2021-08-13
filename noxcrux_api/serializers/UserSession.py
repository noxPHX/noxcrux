from rest_framework.serializers import ModelSerializer, SlugRelatedField, CurrentUserDefault
from noxcrux_api.models.UserSession import UserSession


class UserSessionSerializer(ModelSerializer):

    user = SlugRelatedField(slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        model = UserSession
        fields = ['user', 'session', 'ip', 'user_agent']
