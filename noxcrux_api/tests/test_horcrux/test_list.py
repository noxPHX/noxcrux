from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.serializers.Horcrux import HorcruxSerializer
from noxcrux_api.views.Horcrux import HorcruxList
from django.contrib.auth.models import User


class TestHorcruxList(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.horcrux_data = {'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': cls.test_user}
        cls.url = reverse('horcruxes')

    @classmethod
    def setUpClass(cls):
        super(TestHorcruxList, cls).setUpClass()
        HorcruxList.throttle_classes = ()

    def test_list_horcruxes_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_horcruxes(self):
        self.client.force_login(self.test_user)
        Horcrux.objects.create(**self.horcrux_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Horcrux.objects.count(), 1)

    def test_serializer_horcruxes(self):
        self.client.force_login(self.test_user)
        Horcrux.objects.create(**self.horcrux_data)
        serializer = HorcruxSerializer(Horcrux.objects.all(), many=True)
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)

    def test_unauthorized_put(self):
        self.client.force_login(self.test_user)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_patch(self):
        self.client.force_login(self.test_user)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_delete(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
