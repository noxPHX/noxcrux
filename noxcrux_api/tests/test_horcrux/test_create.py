from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from django.contrib.auth.models import User


class HorcruxCreate(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.horcrux_data = {'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com'}
        cls.url = reverse('horcruxes')

    def test_create_horcrux_not_authenticated(self):
        response = self.client.post(self.url, self.horcrux_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Horcrux.objects.count(), 0)

    def test_create_horcrux(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, self.horcrux_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Horcrux.objects.count(), 1)

    def test_create_horcrux_duplicate_name(self):
        self.client.force_login(self.test_user)
        self.client.post(self.url, self.horcrux_data, format='json')
        response = self.client.post(self.url, self.horcrux_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Horcrux.objects.count(), 1)

    def test_create_horcrux_empty_name(self):
        self.client.force_login(self.test_user)
        data = self.horcrux_data.copy()
        data['name'] = ''
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Horcrux.objects.count(), 0)

    def test_create_horcrux_empty_horcrux(self):
        self.client.force_login(self.test_user)
        data = self.horcrux_data.copy()
        data['horcrux'] = ''
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Horcrux.objects.count(), 0)

    def test_create_horcrux_empty_site(self):
        self.client.force_login(self.test_user)
        data = self.horcrux_data.copy()
        data['site'] = ''
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Horcrux.objects.count(), 0)

    def test_create_horcrux_invalid_site(self):
        self.client.force_login(self.test_user)
        data = self.horcrux_data.copy()
        data['site'] = 'invalid.site'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Horcrux.objects.count(), 0)
