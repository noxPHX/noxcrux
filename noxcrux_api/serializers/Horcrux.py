from rest_framework.serializers import ModelSerializer, CurrentUserDefault, SlugRelatedField
from noxcrux_api.models.Horcrux import Horcrux
from django.http import Http404


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
