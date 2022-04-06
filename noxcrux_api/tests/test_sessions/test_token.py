from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.serializers.UserSession import UserTokenSerializer
from rest_framework.authtoken.models import Token
from noxcrux_api.views.UserSession import UserSessionRevoke


class TestSessionToken(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.data = {'username': 'test', 'password': 'test'}
        cls.url = reverse('api-sessions-token')
        cls.url_token = reverse('token')

    @classmethod
    def setUpClass(cls):
        super(TestSessionToken, cls).setUpClass()
        UserSessionRevoke.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/user/token/')

    def test_unauthorized_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_no_token(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_get_token(self):
        self.client.force_login(self.test_user)
        self.client.post(self.url_token, self.data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['created'])

    def test_serializer(self):
        self.client.force_login(self.test_user)
        self.client.post(self.url_token, self.data)
        serializer = UserTokenSerializer(Token.objects.get())
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)

    def test_not_allowed_post(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_put(self):
        self.client.force_login(self.test_user)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_patch(self):
        self.client.force_login(self.test_user)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_delete(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
