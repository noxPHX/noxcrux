from rest_framework.serializers import ModelSerializer, ValidationError, SlugRelatedField
from noxcrux_api.models.Friend import Friend
from django.http import Http404
from django.contrib.auth.models import User


class FriendSerializer(ModelSerializer):

    class Meta:
        model = Friend
        fields = ['friend']

    friend = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    def validate(self, data):
        request = self.context.get('request', None)
        if not request:
            raise Http404
        if request.user == data['friend']:
            raise ValidationError("Users cannot be friend with themselves.")
        if request.user.friends.filter(friend=data['friend'], validated=False).exists():
            raise ValidationError(f"A friend request was already sent to {data['friend']}")
        if request.user.friends.filter(friend=data['friend'], validated=True).exists():
            raise ValidationError(f"You already are friend with {data['friend']}")
        return super().validate(data)

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['user'] = request.user
            # Create the reversion relationship
            Friend.objects.create(user=validated_data['friend'], friend=request.user)
            return super().create(validated_data)
        else:
            raise Http404
