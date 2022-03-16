from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.views.User import UserList
from noxcrux_api.serializers.User import UserSerializer


class TestUser(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.admin_user = User.objects.create_superuser(username='admin', password='admin')
        cls.url = reverse('users')

    @classmethod
    def setUpClass(cls):
        super(TestUser, cls).setUpClass()
        UserList.throttle_classes = ()

    def test_unauthorized_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_get_list(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    def test_unprivileged_get_list(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_serializer(self):
        self.client.force_login(self.admin_user)
        serializer = UserSerializer(User.objects.all(), many=True)
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)

    def test_unauthorized_put(self):
        self.client.force_login(self.admin_user)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_patch(self):
        self.client.force_login(self.admin_user)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_delete(self):
        self.client.force_login(self.admin_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_trace(self):
        self.client.force_login(self.admin_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
