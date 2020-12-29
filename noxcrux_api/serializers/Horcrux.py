from rest_framework.serializers import ModelSerializer
from noxcrux_api.models.Horcrux import Horcrux
from django.http import Http404


class HorcruxSerializer(ModelSerializer):
    class Meta:
        model = Horcrux
        fields = ['name', 'horcrux', 'site']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['owner_id'] = request.user.id
            return super().create(validated_data)
        else:
            raise Http404
