from noxcrux_api.serializers.UserKeysContainer import UserPublicKeySerializer
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from noxcrux_api.models.UserKeysContainer import UserKeysContainer
from django.http import Http404


@extend_schema_view(
    get=extend_schema(description='Retrieve the public key of the specified user.'),
)
class UserPublicKey(RetrieveAPIView):
    serializer_class = UserPublicKeySerializer

    def get_object(self):
        try:
            return UserKeysContainer.objects.get(user__username=self.kwargs['username'])
        except UserKeysContainer.DoesNotExist:
            raise Http404
