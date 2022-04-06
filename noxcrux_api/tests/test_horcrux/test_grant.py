from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.Friend import Friend
from noxcrux_api.views.Horcrux import HorcruxGrant
from noxcrux_api.serializers.Horcrux import GranteesSerializer
from django.contrib.auth.models import User


class TestHorcruxGrant(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.friend = User.objects.create_user(username='test_friend', password='test_friend')
        cls.third = User.objects.create_user(username='third', password='third')
        Friend.objects.create(user=cls.test_user, friend=cls.friend, validated=True)
        cls.horcrux = Horcrux.objects.create(**{'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': cls.test_user})
        cls.horcrux.grantees.add(cls.friend)
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

    def test_unauthorized_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_patch(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_grantees(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test_friend', response.data['grantees'][0])

    def test_get_serializer(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(GranteesSerializer(self.horcrux).data, response.data)

    def test_get_horcrux_not_found(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('api-horcruxes-grant', args=('Youtube',)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_add_grantees(self):
        Friend.objects.create(user=self.test_user, friend=self.third, validated=True)
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, {'friend': 'third'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.horcrux.grantees.count(), 2)

    def test_put_add_grantees_not_friend(self):
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, {'friend': 'third'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.horcrux.grantees.count(), 1)

    def test_put_add_grantees_self(self):
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, {'friend': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.horcrux.grantees.count(), 1)

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
