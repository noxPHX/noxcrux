from noxcrux_api.serializers.Generator import GeneratorSerializer
from noxcrux_api.models.Generator import Generator
from django.http import Http404
from rest_framework.generics import RetrieveUpdateAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    get=extend_schema(description='Get a generated random horcrux based on preferences.'),
    put=extend_schema(description='Update the generator settings.'),
)
class GeneratorDetail(RetrieveUpdateAPIView):
    serializer_class = GeneratorSerializer

    def get_object(self):
        return self.get_generator(self.request.user)

    def get_generator(self, owner):
        try:
            return Generator.objects.get(owner=owner)
        except Generator.DoesNotExist:
            raise Http404
