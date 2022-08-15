from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.models.Friend import Friend
from noxcrux_api.models.Generator import Generator
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.SharedHorcrux import SharedHorcrux
from noxcrux_api.models.UserKeysContainer import UserKeysContainer
from noxcrux_api.models.UserSession import UserSession
from noxcrux_api.views.User import Profile
from noxcrux_api.serializers.User import UserUpdateSerializer


class TestProfile(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.url = reverse('api-me')

    @classmethod
    def setUpClass(cls):
        super(TestProfile, cls).setUpClass()
        Profile.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/user/me/')

    def test_unauthorized_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_serializer(self):
        self.client.force_login(self.test_user)
        serializer = UserUpdateSerializer(User.objects.get())
        response = self.client.get(self.url)
        self.assertEqual(response.data, serializer.data)

    def test_update_username(self):
        data = {
            'username': 'new_test',
            'old_password': 'test',
            'new_password': 'qugoT6EOPW9PU3bfBB4pUc0n/+IrHd6OdNjJCRP2b1A=',
            'protected_key': 'protected_key',
        }
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(username='test').count(), 0)
        self.assertEqual(User.objects.filter(username='new_test').count(), 1)

    def test_update_username_bad_password(self):
        data = {
            'username': 'new_test',
            'old_password': 'bad_password',
            'new_password': 'qugoT6EOPW9PU3bfBB4pUc0n/+IrHd6OdNjJCRP2b1A=',
            'protected_key': 'protected_key',
        }
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username='test').count(), 1)
        self.assertEqual(User.objects.filter(username='new_test').count(), 0)

    def test_delete_account(self):
        self.client.force_login(self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(username='test').count(), 0)

    def test_delete_account_cascade_friendship(self):
        friend = User.objects.create_user(username='test_friend', password='test_friend')
        Friend.objects.create(user=self.test_user, friend=friend, validated=True)
        self.client.force_login(self.test_user)
        self.client.delete(self.url)
        self.assertEqual(Friend.objects.count(), 0)

    def test_delete_account_cascade_reverse_friendship(self):
        friend = User.objects.create_user(username='test_friend', password='test_friend')
        Friend.objects.create(user=friend, friend=self.test_user, validated=True)
        self.client.force_login(self.test_user)
        self.client.delete(self.url)
        self.assertEqual(Friend.objects.count(), 0)

    def test_delete_account_cascade_generator(self):
        self.assertEqual(Generator.objects.count(), 1)
        self.client.force_login(self.test_user)
        self.client.delete(self.url)
        self.assertEqual(Generator.objects.count(), 0)

    def test_delete_account_cascade_horcrux(self):
        data = {'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': self.test_user}
        Horcrux.objects.create(**data)
        self.client.force_login(self.test_user)
        self.client.delete(self.url)
        self.assertEqual(Horcrux.objects.count(), 0)

    def test_delete_account_cascade_shared_horcrux(self):
        friend = User.objects.create_user(username='test_friend', password='test_friend')
        Friend.objects.create(user=friend, friend=self.test_user, validated=True)
        data = {'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': friend}
        horcrux = Horcrux.objects.create(**data)
        SharedHorcrux.objects.create(horcrux=horcrux, grantee=self.test_user)
        self.client.force_login(self.test_user)
        self.client.delete(self.url)
        self.assertEqual(SharedHorcrux.objects.count(), 0)

    def test_delete_account_double_cascade_shared_horcrux(self):
        friend = User.objects.create_user(username='test_friend', password='test_friend')
        Friend.objects.create(user=friend, friend=self.test_user, validated=True)
        data = {'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': self.test_user}
        horcrux = Horcrux.objects.create(**data)
        SharedHorcrux.objects.create(horcrux=horcrux, grantee=friend)
        self.client.force_login(self.test_user)
        self.client.delete(self.url)
        self.assertEqual(SharedHorcrux.objects.count(), 0)

    def test_delete_account_cascade_keys_container(self):
        self.assertEqual(UserKeysContainer.objects.count(), 1)
        self.client.force_login(self.test_user)
        self.client.delete(self.url)
        self.assertEqual(UserKeysContainer.objects.count(), 0)

    def test_delete_account_cascade_user_session(self):
        self.client.force_login(self.test_user)
        self.assertEqual(UserSession.objects.count(), 1)
        self.client.delete(self.url)
        self.assertEqual(UserSession.objects.count(), 0)

    def test_delete_account_cascade_session(self):
        self.client.force_login(self.test_user)
        self.assertEqual(UserSession.objects.count(), 1)
        self.client.logout()
        self.assertEqual(UserSession.objects.count(), 0)

    def test_not_allowed_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
