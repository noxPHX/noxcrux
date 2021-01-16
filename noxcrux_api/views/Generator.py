from rest_framework import status
from noxcrux_api.serializers.Generator import GeneratorSerializer
from noxcrux_api.models.Generator import Generator
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


class GeneratorDetail(APIView):
    """
    Generate a horcrux or update the preferences
    """

    def get_object(self, owner):
        try:
            return Generator.objects.get(owner=owner)
        except Generator.DoesNotExist:
            raise Http404

    def get(self, request):
        generator = self.get_object(request.user)
        serializer = GeneratorSerializer(generator)
        return Response(serializer.data)

    def put(self, request):
        generator = self.get_object(request.user)
        serializer = GeneratorSerializer(generator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
