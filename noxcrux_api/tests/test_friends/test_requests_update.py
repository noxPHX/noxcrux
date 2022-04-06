from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from noxcrux_api.models.Friend import Friend
from noxcrux_api.views.Friend import FriendRequestUpdate
from django.contrib.auth.models import User


class TestFriendRequestUpdate(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.friend = User.objects.create_user(username='test_friend', password='test_friend')
        cls.url = reverse('api-friends-update', args=('test_friend',))

    @classmethod
    def setUpClass(cls):
        super(TestFriendRequestUpdate, cls).setUpClass()
        FriendRequestUpdate.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/friends/requests/test_friend/')

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

    def test_get_no_request(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_no_request(self):
        self.client.force_login(self.test_user)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_no_request(self):
        self.client.force_login(self.test_user)
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_no_request(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_request(self):
        Friend.objects.create(user=self.friend, friend=self.test_user, validated=False)
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'test_friend')

    def test_accept_request(self):
        Friend.objects.create(user=self.friend, friend=self.test_user, validated=False)
        self.client.force_login(self.test_user)
        response = self.client.put(self.url)
        friend = Friend.objects.get(user=self.friend, friend=self.test_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(friend.validated)

    def test_delete_request(self):
        Friend.objects.create(user=self.friend, friend=self.test_user, validated=False)
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Friend.objects.filter(user=self.friend, friend=self.test_user).count(), 0)

    def test_not_allowed_post(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
