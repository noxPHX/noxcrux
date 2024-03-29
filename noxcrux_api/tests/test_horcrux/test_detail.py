from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.Friend import Friend
from noxcrux_api.models.SharedHorcrux import SharedHorcrux
from noxcrux_api.views.Horcrux import HorcruxDetail
from django.contrib.auth.models import User


class TestHorcruxDetail(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.data = {'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': cls.test_user}
        cls.horcrux = Horcrux.objects.create(**cls.data)
        cls.url = reverse('api-horcrux', args=('Google',))

    @classmethod
    def setUpClass(cls):
        super(TestHorcruxDetail, cls).setUpClass()
        HorcruxDetail.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/horcrux/Google/')

    def test_unauthorized_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_patch(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_horcrux(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Google', response.data['name'])

    def test_get_horcrux_not_found(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('api-horcrux', args=('Youtube',)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_horcrux_name(self):
        self.client.force_login(self.test_user)
        data = self.data.copy()
        data['name'] = 'Google2'
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Google2', response.data['name'])

    def test_put_horcrux_horcrux(self):
        self.client.force_login(self.test_user)
        data = self.data.copy()
        data['horcrux'] = 'a5f8t1'
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('a5f8t1', response.data['horcrux'])

    def test_put_horcrux_site(self):
        self.client.force_login(self.test_user)
        data = self.data.copy()
        data['site'] = 'https://youtube.com'
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('https://youtube.com', response.data['site'])

    def test_put_horcrux_delete_shared_horcrux(self):
        friend = User.objects.create_user(username='test_friend', password='test_friend')
        Friend.objects.create(user=self.test_user, friend=friend, validated=True)
        SharedHorcrux.objects.create(horcrux=self.horcrux, grantee=friend)
        self.client.force_login(self.test_user)
        data = self.data.copy()
        data['name'] = 'Google2'
        self.client.put(self.url, data)
        self.assertEqual(SharedHorcrux.objects.count(), 0)

    def test_put_horcrux_invalid_site(self):
        self.client.force_login(self.test_user)
        data = self.data.copy()
        data['site'] = 'youtube'
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_delete(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_delete_cascade_shared_horcrux(self):
        friend = User.objects.create_user(username='test_friend', password='test_friend')
        Friend.objects.create(user=self.test_user, friend=friend, validated=True)
        SharedHorcrux.objects.create(horcrux=self.horcrux, grantee=friend)
        self.client.force_login(self.test_user)
        self.client.delete(self.url)
        self.assertEqual(SharedHorcrux.objects.count(), 0)

    def test_not_allowed_post(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
