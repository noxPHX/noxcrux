from rest_framework import status
from noxcrux_api.serializers.Friend import FriendSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class FriendList(APIView):
    """
    List all friends, or request a new friendship
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
