from rest_framework.serializers import ModelSerializer, SerializerMethodField
from noxcrux_api.models.Generator import Generator
from drf_spectacular.utils import extend_schema_field


class GeneratorSerializer(ModelSerializer):
    generated_horcrux = SerializerMethodField()

    class Meta:
        model = Generator
        exclude = ['id', 'owner']

    @extend_schema_field(str)
    def get_generated_horcrux(self, generator):
        return generator.generate()
