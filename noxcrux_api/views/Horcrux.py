from noxcrux_api.serializers.Horcrux import HorcruxSerializer, GranteeSerializer
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.SharedHorcrux import SharedHorcrux
from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, DestroyAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Q


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
        return Horcrux.objects.filter(Q(owner=self.request.user), Q(name__icontains=self.kwargs['search']) | Q(site__icontains=self.kwargs['search']))


@extend_schema_view(
    get=extend_schema(description='Retrieve an horcrux instance.'),
    put=extend_schema(description='Update an horcrux instance, revoking all grantees.'),
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
        granted_list = set()
        for shared_horcrux in self.request.user.shared_horcruxes.select_related('horcrux'):
            # Update the horcrux value with the shared one
            shared_horcrux.horcrux.horcrux = shared_horcrux.shared_horcrux
            granted_list.add(shared_horcrux.horcrux)
        return granted_list


@extend_schema_view(
    get=extend_schema(description='List all your granted horcruxes which names match the search query.'),
)
class HorcruxGrantedSearch(ListAPIView):
    serializer_class = HorcruxSerializer

    def get_queryset(self):
        granted_list = set()
        for shared_horcrux in self.request.user.shared_horcruxes.filter(Q(horcrux__name__icontains=self.kwargs['search']) | Q(horcrux__site__icontains=self.kwargs['search'])).select_related('horcrux'):
            granted_list.add(shared_horcrux.horcrux)
        return granted_list


@extend_schema_view(
    get=extend_schema(description='Display all the grantees for the given horcrux.'),
    post=extend_schema(
        description='Add a grantee for the given horcrux.',
        request=GranteeSerializer
    ),
)
class HorcruxGrant(ListCreateAPIView):
    serializer_class = GranteeSerializer

    def get_serializer_context(self):
        try:
            horcrux = Horcrux.objects.get(owner=self.request.user, name=self.kwargs['name'])
        except Horcrux.DoesNotExist:
            raise Http404

        return {
            'horcrux': horcrux,
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_queryset(self):
        return SharedHorcrux.objects.filter(horcrux__owner=self.request.user, horcrux__name=self.kwargs['name'])


@extend_schema_view(
    delete=extend_schema(description='Delete a grantee for the given horcrux.'),
)
class HorcruxRevoke(DestroyAPIView):
    serializer_class = GranteeSerializer

    def get_object(self):
        try:
            return SharedHorcrux.objects.get(horcrux__owner=self.request.user, horcrux__name=self.kwargs['name'], grantee__username=self.kwargs['username'])
        except SharedHorcrux.DoesNotExist:
            raise Http404
