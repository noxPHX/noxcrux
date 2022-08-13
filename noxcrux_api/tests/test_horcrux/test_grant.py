from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.SharedHorcrux import SharedHorcrux
from noxcrux_api.models.Friend import Friend
from noxcrux_api.views.Horcrux import HorcruxGrant
from noxcrux_api.serializers.Horcrux import GranteeSerializer
from django.contrib.auth.models import User


class TestHorcruxGrant(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.friend = User.objects.create_user(username='test_friend', password='test_friend')
        cls.third = User.objects.create_user(username='third', password='third')
        Friend.objects.create(user=cls.test_user, friend=cls.friend, validated=True)
        cls.horcrux = Horcrux.objects.create(**{'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': cls.test_user})
        cls.shared_horcrux = SharedHorcrux.objects.create(horcrux=cls.horcrux, grantee=cls.friend)
        cls.url = reverse('api-horcruxes-grant', args=('Google',))

    @classmethod
    def setUpClass(cls):
        super(TestHorcruxGrant, cls).setUpClass()
        HorcruxGrant.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/horcrux/shared/Google/')

    def test_unauthorized_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_grantees(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test_friend', response.data[0]['grantee'])

    def test_get_serializer(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual([GranteeSerializer(self.shared_horcrux).data], response.json())

    def test_get_horcrux_not_found(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('api-horcruxes-grant', args=('Youtube',)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_add_grantees(self):
        Friend.objects.create(user=self.test_user, friend=self.third, validated=True)
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'grantee': 'third', 'shared_horcrux': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SharedHorcrux.objects.count(), 2)

    def test_post_add_grantees_not_friend(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'grantee': 'third', 'shared_horcrux': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SharedHorcrux.objects.count(), 1)

    def test_post_add_grantees_not_exists(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'grantee': 'nonexistent', 'shared_horcrux': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SharedHorcrux.objects.count(), 1)

    def test_post_add_grantees_self(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'grantee': 'third', 'shared_horcrux': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SharedHorcrux.objects.count(), 1)

    def test_post_horcrux_not_found(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('api-horcruxes-grant', args=('Youtube',)), {'grantee': 'third', 'shared_horcrux': 'test'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
