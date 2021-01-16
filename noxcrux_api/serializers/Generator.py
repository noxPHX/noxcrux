from rest_framework.serializers import ModelSerializer, SerializerMethodField
from noxcrux_api.models.Generator import Generator


class GeneratorSerializer(ModelSerializer):
    generated_horcrux = SerializerMethodField()

    class Meta:
        model = Generator
        exclude = ['id', 'owner']

    def get_generated_horcrux(self, generator):
        return generator.generate()
