from django.contrib.auth.models import User
from rest_framework import status
from noxcrux_api.serializers.User import UserListSerializer, UserCreateSerializer, PasswordUpdateSerializer, UserUpdateSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response
from noxcrux_api.permissions import UsersPermissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get=extend_schema(description='List all users.'),
    post=extend_schema(description='Register a new user.'),
)
class UserList(ListCreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [UsersPermissions]

    # FIXME, better way of swapping Serializer ?
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if settings.REGISTRATION_OPEN is False:
            return Response({"error": "Registrations are closed."}, status=status.HTTP_400_BAD_REQUEST)
        return super(UserList, self).post(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(description='Get my account information.'),
    put=extend_schema(description='Update my username.'),
    delete=extend_schema(description='Delete my account.'),
)
class Profile(RetrieveUpdateDestroyAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    # TODO refacto with class below
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            user = serializer.save()
            if hasattr(user, 'auth_token'):
                user.auth_token.delete()
            token, created = Token.objects.get_or_create(user=user)
            update_session_auth_hash(request, user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    put=extend_schema(description='Update my password.'),
)
class PasswordUpdate(UpdateAPIView):
    serializer_class = PasswordUpdateSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            user = serializer.save()
            if hasattr(user, 'auth_token'):
                user.auth_token.delete()
            token, created = Token.objects.get_or_create(user=user)
            update_session_auth_hash(request, user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
