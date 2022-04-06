from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.Friend import Friend
from noxcrux_api.views.Horcrux import HorcruxRevoke


class TestHorcruxRevoke(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.friend = User.objects.create_user(username='test_friend', password='test_friend')
        Friend.objects.create(user=cls.test_user, friend=cls.friend, validated=True)
        cls.horcrux = Horcrux.objects.create(**{'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': cls.test_user})
        cls.horcrux.grantees.add(cls.friend)
        cls.url = reverse('api-horcruxes-granted-revoke', args=('Google', 'test_friend'))

    @classmethod
    def setUpClass(cls):
        super(TestHorcruxRevoke, cls).setUpClass()
        HorcruxRevoke.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/horcrux/shared/Google/test_friend/')

    def test_unauthorized_revoke(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_revoke(self):
        self.client.force_login(self.test_user)
        self.assertEqual(self.horcrux.grantees.count(), 1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.horcrux.grantees.count(), 0)

    def test_revoke_horcrux_not_found(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(reverse('api-horcruxes-granted-revoke', args=('Youtube', 'test_friend')))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.horcrux.grantees.count(), 1)

    def test_not_allowed_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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

    def test_not_allowed_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
