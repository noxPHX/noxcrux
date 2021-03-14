from django.contrib.auth.models import User
from rest_framework import status
from noxcrux_api.serializers.User import UserSerializer, UserUpdateSerializer, PasswordUpdateSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.response import Response
from noxcrux_api.permissions import UsersPermissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view


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
        if settings.REGISTRATION_OPEN is False:
            return Response({"error": "Registrations are closed."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(description='Get a user or delete it\'s account'),
)
class Profile(RetrieveDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        try:
            return User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            raise Http404


class UserUpdate(APIView):
    """
    Update a user's username
    """

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordUpdate(APIView):
    """
    Update a user's password
    """

    def put(self, request):
        serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            if hasattr(user, 'auth_token'):
                user.auth_token.delete()
            token, created = Token.objects.get_or_create(user=user)
            update_session_auth_hash(request, user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
