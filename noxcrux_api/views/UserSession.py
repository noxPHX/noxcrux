from noxcrux_api.models.UserSession import UserSession
from django.contrib.sessions.models import Session
from noxcrux_api.serializers.UserSession import UserSessionSerializer
from rest_framework.generics import ListAPIView, DestroyAPIView
from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get=extend_schema(description='List all the web sessions for the current user'),
)
class UserSessionList(ListAPIView):
    serializer_class = UserSessionSerializer

    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)


@extend_schema_view(
    delete=extend_schema(description='Revoke the specified session'),
)
class UserSessionRevoke(DestroyAPIView):
    serializer_class = UserSessionSerializer

    def get_object(self):
        try:
            return Session.objects.get(session_key=self.kwargs['session'])
        except UserSession.DoesNotExist:
            raise Http404