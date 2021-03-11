from rest_framework import status
from noxcrux_api.serializers.Horcrux import HorcruxSerializer, GranteeSerializer, GranteesSerializer
from noxcrux_api.models.Horcrux import Horcrux
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User


class HorcruxList(ListCreateAPIView):
    """
    get:
    List all your personal horcruxes.

    post:
    Create a new horcrux.
    """
    serializer_class = HorcruxSerializer

    def get_queryset(self):
        return Horcrux.objects.filter(owner=self.request.user)


class HorcruxDetail(RetrieveUpdateDestroyAPIView):
    """
    get:
    Retrieve an horcrux instance.

    put:
    Update an horcrux instance.

    delete:
    Remove an horcrux instance.
    """
    serializer_class = HorcruxSerializer

    def get_object(self):
        return self.get_horcrux(self.kwargs['name'], self.request.user)

    def get_horcrux(self, name, owner):
        try:
            return Horcrux.objects.get(name=name, owner=owner)
        except Horcrux.DoesNotExist:
            raise Http404


class HorcruxGrantedList(APIView):
    """
    get:
    List all your granted horcruxes.
    """

    def get(self, request):
        horcruxes = request.user.shared_horcruxes.all()
        serializer = HorcruxSerializer(horcruxes, many=True)
        return Response(serializer.data)


# FIXME better way to handle those serializers ?
class HorcruxGrant(APIView):
    """
    get:
    Display all the grantees for the given horcrux.

    put:
    Add a grantee for the given horcrux.

    delete:
    Delete a grantee for the given horcrux.
    """

    def get_object(self, name, owner):
        try:
            return Horcrux.objects.get(name=name, owner=owner)
        except Horcrux.DoesNotExist:
            raise Http404

    def get(self, request, name):
        horcrux = self.get_object(name, request.user)
        serializer = GranteesSerializer(horcrux)
        return Response(serializer.data)

    def put(self, request, name):
        horcrux = self.get_object(name, request.user)
        serializer = GranteeSerializer(horcrux, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(GranteesSerializer(horcrux).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, username):
        horcrux = self.get_object(name, request.user)
        horcrux.grantees.remove(User.objects.get(username=username))
        return Response(status=status.HTTP_204_NO_CONTENT)
