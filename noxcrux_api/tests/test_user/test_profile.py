from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.views.User import UserList
from noxcrux_api.serializers.User import UserUpdateSerializer


class TestProfile(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.url = reverse('api-me')

    @classmethod
    def setUpClass(cls):
        super(TestProfile, cls).setUpClass()
        UserList.throttle_classes = ()

    def test_unauthorized_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_serializer(self):
        self.client.force_login(self.test_user)
        serializer = UserUpdateSerializer(User.objects.get())
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)

    def test_update_username(self):
        data = {'username': 'new_test'}
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)
        self.assertEqual(User.objects.filter(username='test').count(), 0)
        self.assertEqual(User.objects.filter(username='new_test').count(), 1)

    def test_delete_account(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(username='test').count(), 0)

    def test_not_allowed_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
