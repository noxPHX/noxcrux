from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Friend import Friend
from noxcrux_api.serializers.Friend import FriendSerializer
from noxcrux_api.views.Friend import FriendList
from django.contrib.auth.models import User


class TestFriendList(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.friend = User.objects.create_user(username='test_friend', password='test_friend')
        cls.url = reverse('api-friends')

    @classmethod
    def setUpClass(cls):
        super(TestFriendList, cls).setUpClass()
        FriendList.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/friends/')

    def test_unauthorized_list_friends(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_no_friends(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_list_friends(self):
        Friend.objects.create(user=self.test_user, friend=self.friend, validated=True)
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['friend'], 'test_friend')

    def test_serializer_friends(self):
        Friend.objects.create(user=self.test_user, friend=self.friend, validated=True)
        self.client.force_login(self.test_user)
        serializer = FriendSerializer(self.test_user.friends, many=True)
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)

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
