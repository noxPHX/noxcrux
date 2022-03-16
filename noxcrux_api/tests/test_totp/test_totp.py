from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from noxcrux_api.views.OTP import TOTPView
from noxcrux_api.serializers.OTP import TOTPSerializer
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.oath import TOTP


class TestTOTP(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.url = reverse('api-totp')

    @classmethod
    def setUpClass(cls):
        super(TestTOTP, cls).setUpClass()
        TOTPView.throttle_classes = ()

    def test_get_device(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TOTPDevice.objects.count(), 1)

    # FIXME For some reason the totpdevice_set is empty
    """
    def test_totp_serializer(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        serializer = TOTPSerializer(self.test_user.totpdevice_set.get())
        self.assertEqual(response.data, serializer.data)
    """

    def test_confirm_device(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        key = TOTPDevice.objects.get(user=self.test_user).key
        key = key.encode()
        totp = TOTP(key)
        self.assertTrue(totp.verify(totp.token()))
        # FIXME For some reason the token as argument does not work
        # response = self.client.put(self.url, {'totp_code': str(totp.token())})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(TOTPDevice.objects.filter(confirmed=True).count(), 1)

    def test_delete_unconfirmed_device(self):
        self.client.force_login(self.test_user)
        self.client.get(self.url)
        self.assertEqual(TOTPDevice.objects.count(), 1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TOTPDevice.objects.count(), 1)

    # FIXME Idem
    """
    def test_delete_confirmed_device(self):
        self.client.force_login(self.test_user)
        self.client.get(self.url)
        self.assertEqual(TOTPDevice.objects.count(), 1)
        device = TOTPDevice.objects.get()
        device.confirmed = True
        device.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TOTPDevice.objects.count(), 0)
    """

    def test_unauthorized_post(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_trace(self):
        self.client.force_login(self.test_user)
        response = self.client.trace(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
