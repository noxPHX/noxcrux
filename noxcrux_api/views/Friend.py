from rest_framework import status
from noxcrux_api.serializers.Friend import FriendSerializer, FriendRequestSerializer
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.http import Http404
from noxcrux_api.models.Friend import Friend
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get=extend_schema(description='List all your friends.'),
    post=extend_schema(description='Send a friend request.'),
)
class FriendList(ListCreateAPIView):
    serializer_class = FriendSerializer

    def get_queryset(self):
        return self.request.user.friends.filter(validated=True)


@extend_schema_view(
    delete=extend_schema(description='Remove a friendship.'),
)
class FriendDestroy(DestroyAPIView):
    serializer_class = FriendSerializer

    def delete(self, request, *args, **kwargs):
        try:
            friendship = request.user.friends.get(friend__username=self.kwargs['username'], validated=True)
        except Friend.DoesNotExist:
            raise Http404
        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(description='List all your friend requests.'),
)
class FriendRequestsList(ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return self.request.user.reverse_friends.filter(validated=False)


@extend_schema_view(
    get=extend_schema(description='Display a friend request'),
    put=extend_schema(description='Accept or deny a friend request.'),
    delete=extend_schema(description='Delete a request.'),
)
class FriendRequestUpdate(RetrieveUpdateDestroyAPIView):
    serializer_class = FriendRequestSerializer

    def get_object(self):
        try:
            return self.request.user.reverse_friends.get(user__username=self.kwargs['username'], validated=False)
        except Friend.DoesNotExist:
            raise Http404
