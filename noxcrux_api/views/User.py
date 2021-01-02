from django.contrib.auth.models import User
from rest_framework import status
from noxcrux_api.serializers.User import UserSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from noxcrux_api.permissions import UsersPermissions, UserUpdatePermissions
from django.http import Http404


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


# TODO user password update, user delete, and according permissions/serializers
class UserUpdate(APIView):
    """
    Retrieve a user or update its username or password
    """
    permission_classes = [UserUpdatePermissions]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
