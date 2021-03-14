from noxcrux_api.serializers.Generator import GeneratorSerializer
from noxcrux_api.models.Generator import Generator
from django.http import Http404
from rest_framework.generics import RetrieveUpdateAPIView


class GeneratorDetail(RetrieveUpdateAPIView):
    """
    get:
    Get a generated random horcrux based on preferences.

    put:
    Update the generator settings.
    """
    serializer_class = GeneratorSerializer

    def get_object(self):
        return self.get_generator(self.request.user)

    def get_generator(self, owner):
        try:
            return Generator.objects.get(owner=owner)
        except Generator.DoesNotExist:
            raise Http404
