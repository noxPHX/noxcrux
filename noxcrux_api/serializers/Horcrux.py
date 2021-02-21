from rest_framework.serializers import Serializer, ModelSerializer, CurrentUserDefault, SlugRelatedField, ValidationError, CharField
from noxcrux_api.models.Horcrux import Horcrux
from django.http import Http404
from django.contrib.auth.models import User


class HorcruxSerializer(ModelSerializer):
    """
    owner needs to be declared explicitly to check against unique together constraint
    """
    owner = SlugRelatedField(slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Horcrux
        fields = ['name', 'horcrux', 'site', 'owner']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['owner_id'] = request.user.id
            return super().create(validated_data)
        else:
            raise Http404


class GranteesSerializer(ModelSerializer):

    class Meta:
        model = Horcrux
        fields = ['grantees']

    grantees = SlugRelatedField(slug_field='username', queryset=User.objects.all(), many=True)


class GranteeSerializer(Serializer):

    granted = CharField(required=True, max_length=150)

    def validate(self, data):
        request = self.context.get('request', None)
        if not request:
            raise Http404
        if request.user.username == data['granted']:
            raise ValidationError("Users cannot grant themselves horcruxes.")
        if not request.user.friends.filter(friend__username=data['granted'], validated=True).exists():
            raise ValidationError(f"You are not friend with {data['granted']}")
        return super().validate(data)

    def update(self, instance, validated_data):
        self.instance.grantees.add(User.objects.get(username=validated_data['granted']))
        return instance
