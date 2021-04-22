from rest_framework import status
from noxcrux_api.serializers.Horcrux import HorcruxSerializer, GranteeSerializer, GranteesSerializer
from noxcrux_api.models.Horcrux import Horcrux
from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get=extend_schema(description='List all your personal horcruxes.'),
    post=extend_schema(description='Create a new horcrux.'),
)
class HorcruxList(ListCreateAPIView):
    serializer_class = HorcruxSerializer

    def get_queryset(self):
        return Horcrux.objects.filter(owner=self.request.user)


@extend_schema_view(
    get=extend_schema(description='List all the horcruxes which names match the search query.'),
)
class HorcruxSearch(ListAPIView):
    serializer_class = HorcruxSerializer

    def get_queryset(self):
        return Horcrux.objects.filter(owner=self.request.user, name__icontains=self.kwargs['name'])


@extend_schema_view(
    get=extend_schema(description='Retrieve an horcrux instance.'),
    put=extend_schema(description='Update an horcrux instance.'),
    delete=extend_schema(description='Remove an horcrux instance.'),
)
class HorcruxDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = HorcruxSerializer

    def get_object(self):
        return self.get_horcrux(self.kwargs['name'], self.request.user)

    def get_horcrux(self, name, owner):
        try:
            return Horcrux.objects.get(name=name, owner=owner)
        except Horcrux.DoesNotExist:
            raise Http404


@extend_schema_view(
    get=extend_schema(description='List all your granted horcruxes.'),
)
class HorcruxGrantedList(ListAPIView):
    serializer_class = HorcruxSerializer

    def get_queryset(self):
        return self.request.user.shared_horcruxes.all()


@extend_schema_view(
    get=extend_schema(description='List all your granted horcruxes which names match the search query.'),
)
class HorcruxGrantedSearch(ListAPIView):
    serializer_class = HorcruxSerializer

    def get_queryset(self):
        return self.request.user.shared_horcruxes.filter(name__icontains=self.kwargs['name'])


@extend_schema_view(
    get=extend_schema(description='Display all the grantees for the given horcrux.'),
    put=extend_schema(
        description='Add a grantee for the given horcrux.',
        request=GranteeSerializer
    ),
)
class HorcruxGrant(RetrieveUpdateAPIView):
    serializer_class = GranteesSerializer

    def get_object(self):
        try:
            return Horcrux.objects.get(name=self.kwargs['name'], owner=self.request.user)
        except Horcrux.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        horcrux = self.get_object()
        serializer = GranteeSerializer(horcrux, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(GranteesSerializer(horcrux).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    delete=extend_schema(description='Delete a grantee for the given horcrux.'),
)
class HorcruxRevoke(DestroyAPIView):
    serializer_class = GranteesSerializer

    def get_object(self):
        try:
            return Horcrux.objects.get(name=self.kwargs['name'], owner=self.request.user)
        except Horcrux.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        horcrux = self.get_object()
        horcrux.grantees.remove(User.objects.get(username=self.kwargs['username']))
        return Response(status=status.HTTP_204_NO_CONTENT)
