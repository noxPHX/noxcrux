from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.views.Horcrux import HorcruxSearch
from django.contrib.auth.models import User


class TestHorcruxSearch(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        Horcrux.objects.create(**{'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': cls.test_user})
        cls.url = reverse('api-horcruxes-search', args=('goo',))

    @classmethod
    def setUpClass(cls):
        super(TestHorcruxSearch, cls).setUpClass()
        HorcruxSearch.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/horcruxes/search/goo/')

    def test_unauthorized_search(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_horcruxes_by_name(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data[0])
        self.assertIsNotNone(response.data[0]['name'])
        self.assertEqual('Google', response.data[0]['name'])

    def test_search_horcruxes_by_site(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('api-horcruxes-search', args=('com',)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data[0])
        self.assertIsNotNone(response.data[0]['name'])
        self.assertEqual('Google', response.data[0]['name'])

    def test_search_horcruxes_not_found(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('api-horcruxes-search', args=('bad',)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

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
