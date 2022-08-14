import django.core.exceptions
from rest_framework.serializers import Serializer, ModelSerializer, CurrentUserDefault, SlugRelatedField, ValidationError, CharField
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.SharedHorcrux import SharedHorcrux
from django.http import Http404
from django.contrib.auth.models import User
from django.core.validators import URLValidator


class HorcruxSerializer(ModelSerializer):
    """
    owner needs to be declared explicitly to check against unique together constraint
    """
    owner = SlugRelatedField(slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Horcrux
        fields = ['name', 'horcrux', 'site', 'owner']

    def validate_site(self, value):
        try:
            URLValidator()(value)
        except django.core.exceptions.ValidationError as e:
            raise ValidationError(e)
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner_id'] = request.user.id
        return super().create(validated_data)


class GranteeSerializer(ModelSerializer):

    class Meta:
        model = SharedHorcrux
        fields = ['grantee', 'shared_horcrux']
        extra_kwargs = {
            'shared_horcrux': {'write_only': True},
        }

    grantee = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    def validate(self, data):
        request = self.context.get('request')
        if request.user.username == data['grantee'].username:
            raise ValidationError("Users cannot grant themselves horcruxes.")
        if not request.user.friends.filter(friend=data['grantee'], validated=True).exists():
            raise ValidationError(f"You are not friend with {data['grantee']}")
        if SharedHorcrux.objects.filter(grantee=data['grantee'], horcrux=self.context['horcrux']).exists():
            raise ValidationError(f"{self.context['horcrux']} already shared with {data['grantee']}")
        return super().validate(data)

    def create(self, validated_data):
        validated_data['horcrux'] = self.context['horcrux']
        return super().create(validated_data)
