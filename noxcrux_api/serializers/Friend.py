from rest_framework.serializers import ModelSerializer, ValidationError, SlugRelatedField, BooleanField
from noxcrux_api.models.Friend import Friend
from django.contrib.auth.models import User


class FriendSerializer(ModelSerializer):

    class Meta:
        model = Friend
        fields = ['friend']

    friend = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    def validate(self, data):
        request = self.context.get('request')
        if request.user == data['friend']:
            raise ValidationError("Users cannot be friend with themselves.")
        if request.user.friends.filter(friend=data['friend'], validated=False).exists():
            raise ValidationError(f"A friend request was already sent to {data['friend']}")
        if request.user.friends.filter(friend=data['friend'], validated=True).exists():
            raise ValidationError(f"You already are friend with {data['friend']}")
        return super().validate(data)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class FriendRequestSerializer(ModelSerializer):

    class Meta:
        model = Friend
        fields = ['user', 'validated']

    user = SlugRelatedField(slug_field='username', read_only=True)
    validated = BooleanField(required=False, default=True)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # Create the reverse relationship
        Friend.objects.create(user=request.user, friend=instance.user, validated=True)
        return super().update(instance, validated_data)
