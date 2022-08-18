from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.models.UserKeysContainer import UserKeysContainer
from noxcrux_api.views.UserKeysContainer import UserPublicKey
from noxcrux_api.serializers.UserKeysContainer import UserPublicKeySerializer


class TestUserPublicKey(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.url = reverse('api-user-pk', args=('test',))

    @classmethod
    def setUpClass(cls):
        super(TestUserPublicKey, cls).setUpClass()
        UserPublicKey.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/users/test/')

    def test_unauthorized_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_serializer(self):
        self.client.force_login(self.test_user)
        serializer = UserPublicKeySerializer(UserKeysContainer.objects.first())
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)

    def test_get_not_found(self):
        self.client.force_login(self.test_user)
        UserKeysContainer.objects.first().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
