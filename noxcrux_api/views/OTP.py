from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import devices_for_user


def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


class TOTPView(APIView):
    """
    Set up a new TOTP device
    """
    def get(self, request):
        device = get_user_totp_device(request.user)
        if not device:
            device = request.user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)
    """
    Verify/Enable a TOTP device
    """
    def post(self, request, totp_code):
        device = get_user_totp_device(request.user)
        if not device:
            return Response(dict(errors=['You have not setup two factor authentication.']), status=status.HTTP_400_BAD_REQUEST)
        if device.confirmed:
            return Response(dict(errors=['You already have confirmed your device.']), status=status.HTTP_400_BAD_REQUEST)
        if device.verify_token(totp_code):
            device.confirmed = True
            device.save()
            return Response(status=status.HTTP_200_OK)
        return Response(dict(errors=dict(token=['Invalid TOTP Token.'])), status=status.HTTP_400_BAD_REQUEST)
