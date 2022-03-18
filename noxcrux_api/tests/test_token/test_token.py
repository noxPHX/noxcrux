from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.views.Token import TokenDetail
from rest_framework.authtoken.models import Token
from noxcrux.utils import disable_logging


class TestToken(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.data = {'username': 'test', 'password': 'test'}
        cls.url = reverse('token')

    @classmethod
    def setUpClass(cls):
        super(TestToken, cls).setUpClass()
        TokenDetail.throttle_classes = ()

    def test_create_token(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], Token.objects.get().key)
        self.assertEqual(Token.objects.count(), 1)

    def test_delete_token(self):
        self.client.post(self.url, self.data)
        self.assertEqual(Token.objects.count(), 1)
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Token.objects.count(), 0)

    @disable_logging
    def test_create_invalid_username(self):
        data = self.data.copy()
        data['username'] = 'azer'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Token.objects.count(), 0)

    @disable_logging
    def test_create_invalid_password(self):
        data = self.data.copy()
        data['password'] = 'azer'
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Token.objects.count(), 0)

    def test_create_empty_username(self):
        data = self.data.copy()
        data['username'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Token.objects.count(), 0)

    def test_create_empty_password(self):
        data = self.data.copy()
        data['password'] = ''
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Token.objects.count(), 0)

    def test_not_allowed_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_patch(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_trace(self):
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
