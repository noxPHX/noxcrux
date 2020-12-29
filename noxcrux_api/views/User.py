from django.contrib.auth.models import User
from rest_framework import status
from noxcrux_api.serializers.User import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from noxcrux_api.permissions import UsersPermissions


class UserList(APIView):
    """
    List all users, or create a new user
    """
    permission_classes = [UsersPermissions]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
