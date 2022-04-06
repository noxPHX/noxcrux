from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Friend import Friend
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

    def test_unauthorized_friend_request(self):
        response = self.client.post(self.url, {'friend': 'test_friend'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Friend.objects.count(), 0)

    def test_friend_request(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'friend': 'test_friend'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friend.objects.filter(validated=False).count(), 1)

    def test_empty_request(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'friend': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friend.objects.filter(validated=False).count(), 0)

    def test_invalid_request(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'friend': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friend.objects.filter(validated=False).count(), 0)

    def test_self_request(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'friend': 'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friend.objects.filter(validated=False).count(), 0)

    def test_double_request(self):
        self.client.force_login(self.test_user)
        self.client.post(self.url, {'friend': 'test_friend'})
        response = self.client.post(self.url, {'friend': 'test_friend'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friend.objects.filter(validated=False).count(), 1)

    def test_already_friend(self):
        Friend.objects.create(user=self.test_user, friend=self.friend, validated=True)
        self.client.force_login(self.test_user)
        response = self.client.post(self.url, {'friend': 'test_friend'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friend.objects.filter(validated=True).count(), 1)
