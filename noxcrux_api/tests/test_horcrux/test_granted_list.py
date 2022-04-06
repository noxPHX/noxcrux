from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.Friend import Friend
from noxcrux_api.views.Horcrux import HorcruxGrantedList
from django.contrib.auth.models import User


class TestHorcruxGrantedList(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.friend = User.objects.create_user(username='test_friend', password='test_friend')
        Friend.objects.create(user=cls.test_user, friend=cls.friend, validated=True)
        cls.url = reverse('api-horcruxes-granted')

    @classmethod
    def setUpClass(cls):
        super(TestHorcruxGrantedList, cls).setUpClass()
        HorcruxGrantedList.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/horcruxes/granted/')

    def test_unauthorized_list_granted_horcruxes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_no_granted_horcruxes(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_list_granted_horcruxes(self):
        self.client.force_login(self.test_user)
        horcrux = Horcrux.objects.create(**{'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': self.friend})
        horcrux.grantees.add(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test_friend', response.data[0]['owner'])

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
