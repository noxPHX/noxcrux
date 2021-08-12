from noxcrux_api.models.UserSession import UserSession
from noxcrux_api.serializers.UserSession import UserSessionSerializer
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get=extend_schema(description='List all the web sessions for the current user'),
)
class UserSessionList(ListAPIView):
    serializer_class = UserSessionSerializer

    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)
