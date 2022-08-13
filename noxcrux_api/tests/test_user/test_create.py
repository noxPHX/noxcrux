from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.views.User import UserList
from django.test.utils import override_settings


class TestUserCreate(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'username': 'test',
            'password': 'qugoT6EOPW9PU3bfBB4pUc0n/+IrHd6OdNjJCRP2b1A=',
            'public_key': 'public_key',
            'protected_key': 'protected_key',
            'iv': 'iv',
        }
        cls.url = reverse('users')

    @classmethod
    def setUpClass(cls):
        super(TestUserCreate, cls).setUpClass()
        UserList.throttle_classes = ()

    def test_create_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    @override_settings(REGISTRATION_OPEN=False)
    def test_create_user_registration_closed(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_duplicate_username(self):
        self.client.post(self.url, self.data)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_empty_username(self):
        data = self.data.copy()
        data['username'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_empty_password(self):
        data = self.data.copy()
        data['password'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_invalid_password(self):
        data = self.data.copy()
        data['password'] = 'a'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Anomalous", response.data['password'][0])
        self.assertEqual(User.objects.count(), 0)
