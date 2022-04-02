from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.Generator import Generator
from django.contrib.auth.models import User


class TestModels(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.horcrux_data = {'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': cls.test_user}

    def test_horcrux_str(self):
        horcrux = Horcrux.objects.create(**self.horcrux_data)
        self.assertEqual('Google', str(horcrux))

    def test_generator_str(self):
        self.assertEqual('test', str(Generator.objects.get()))
