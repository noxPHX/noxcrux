from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.models.UserSession import UserSession
from noxcrux_api.views.UserSession import UserSessionRevoke


class TestSessionRevoke(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.url = reverse('api-sessions-revoke', args=('test',))

    @classmethod
    def setUpClass(cls):
        super(TestSessionRevoke, cls).setUpClass()
        UserSessionRevoke.throttle_classes = ()

    def test_url(self):
        self.assertEqual(self.url, '/api/user/sessions/test/')

    def test_unauthorized_revoke(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_revoke(self):
        self.client.force_login(self.test_user)
        self.assertEqual(UserSession.objects.count(), 1)
        session = UserSession.objects.get(user=self.test_user).session
        url = reverse('api-sessions-revoke', args=(session,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserSession.objects.count(), 0)

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
