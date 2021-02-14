from rest_framework import status
from noxcrux_api.serializers.Friend import FriendSerializer, FriendRequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from noxcrux_api.models.Friend import Friend


class FriendList(APIView):
    """
    List all friends, request a new friendship or delete a friend
    """

    def get(self, request):
        friends = request.user.friends.filter(validated=True)
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FriendSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        try:
            friendship = request.user.friends.get(friend__username=username, validated=True)
        except Friend.DoesNotExist:
            raise Http404
        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendRequest(APIView):
    """
    List all friend requests, respond to a request, or delete a request
    """

    def get_object(self, request, username):
        try:
            return request.user.reverse_friends.get(user__username=username, validated=False)
        except Friend.DoesNotExist:
            raise Http404

    def get(self, request):
        friends = request.user.reverse_friends.filter(validated=False)
        serializer = FriendRequestSerializer(friends, many=True)
        return Response(serializer.data)

    def put(self, request, username):
        friendship = self.get_object(request, username)
        serializer = FriendRequestSerializer(friendship, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        friendship = self.get_object(request, username)
        friendship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
