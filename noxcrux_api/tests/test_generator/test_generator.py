from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.views.Generator import GeneratorDetail
from noxcrux_api.models.Generator import Generator, ALLOWED_SYMBOLS
from noxcrux_api.serializers.Generator import GeneratorSerializer


class TestGenerator(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.data = {'username': 'test', 'password': 'test'}
        cls.url = reverse('generate')

    @classmethod
    def setUpClass(cls):
        super(TestGenerator, cls).setUpClass()
        GeneratorDetail.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/generator/')

    def test_unauthorized_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_patch(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_generator_exists(self):
        self.assertEqual(Generator.objects.count(), 1)

    def test_get_generated(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['generated_horcrux'])

    def test_get_generated_no_generator(self):
        # For some reason the generator is deleted
        Generator.objects.get().delete()
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_serializer(self):
        self.client.force_login(self.test_user)
        serializer = GeneratorSerializer(Generator.objects.get())
        response = self.client.get(self.url)
        self.assertEqual(response.data['upper'], serializer.data['upper'])
        self.assertEqual(response.data['numeric'], serializer.data['numeric'])
        self.assertEqual(response.data['symbol'], serializer.data['symbol'])
        self.assertEqual(response.data['size'], serializer.data['size'])

    def test_put_generator_no_upper(self):
        self.client.force_login(self.test_user)
        # Increase size to reduce luck factor
        response = self.client.put(self.url, {'upper': False, 'numeric': True, 'symbol': True, 'size': 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(any(char.isupper() for char in response.data['generated_horcrux']))

    def test_put_generator_no_numeric(self):
        self.client.force_login(self.test_user)
        # Increase size to reduce luck factor
        response = self.client.put(self.url, {'upper': True, 'numeric': False, 'symbol': True, 'size': 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(any(char.isdigit() for char in response.data['generated_horcrux']))

    def test_put_generator_no_symbol(self):
        self.client.force_login(self.test_user)
        # Increase size to reduce luck factor
        response = self.client.put(self.url, {'upper': True, 'numeric': True, 'symbol': False, 'size': 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(any(char in ALLOWED_SYMBOLS for char in response.data['generated_horcrux']))

    def test_put_generator_everything(self):
        self.client.force_login(self.test_user)
        # Increase size to reduce luck factor
        response = self.client.put(self.url, {'upper': True, 'numeric': True, 'symbol': True, 'size': 50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['generated_horcrux']), 50)
        self.assertTrue(any(char in ALLOWED_SYMBOLS for char in response.data['generated_horcrux']))
        self.assertTrue(any(char.isdigit() for char in response.data['generated_horcrux']))
        self.assertTrue(any(char.isupper() for char in response.data['generated_horcrux']))

    def test_not_allowed_post(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_delete(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
