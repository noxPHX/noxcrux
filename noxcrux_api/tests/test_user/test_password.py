from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.views.User import PasswordUpdate


# TODO check anomalous passwords
class TestPassword(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.password = 'qugoT6EOPW9PU3bfBB4pUc0n/+IrHd6OdNjJCRP2b1A='
        cls.new_password = 'THrDBF9lb4i8qty1u5jib7pui2LhveOOXDWwrCMXzgE='
        cls.test_user = User.objects.create_user(username='test', password=cls.password)
        cls.data = {'old_password': cls.password, 'new_password1': cls.new_password, 'new_password2': cls.new_password, 'protected_key': 'test_key'}
        cls.url = reverse('api-password')

    @classmethod
    def setUpClass(cls):
        super(TestPassword, cls).setUpClass()
        PasswordUpdate.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/user/password/')

    def test_unauthorized_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_password(self):
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password(self.new_password))

    def test_update_password_token_refreshed(self):
        token_url = reverse('token')
        response = self.client.post(token_url, {'username': 'test', 'password': self.password})
        old_token = response.data['token']
        self.client.force_login(self.test_user)
        self.client.put(self.url, self.data)
        response = self.client.post(token_url, {'username': 'test', 'password': self.new_password})
        new_token = response.data['token']
        self.assertIsNotNone(new_token)
        self.assertNotEqual(old_token, new_token)

    def test_update_bad_password(self):
        data = self.data.copy()
        data['old_password'] = 'bad_test'
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.test_user.check_password(self.password))

    def test_update_mismatching_passwords(self):
        data = self.data.copy()
        data['new_password2'] = 'bad_test'
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.test_user.check_password(self.password))

    def test_update_empty_password(self):
        data = self.data.copy()
        data['old_password'] = ''
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.test_user.check_password(self.password))

    def test_update_empty_password1(self):
        data = self.data.copy()
        data['new_password1'] = ''
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.test_user.check_password(self.password))

    def test_update_empty_password2(self):
        data = self.data.copy()
        data['new_password2'] = ''
        self.client.force_login(self.test_user)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(self.test_user.check_password(self.password))

    def test_not_allowed_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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
