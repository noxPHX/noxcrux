from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import devices_for_user
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


@extend_schema_view(
    get=extend_schema(description='Set up a new TOTP device'),
    post=extend_schema(
        description='Verify/Enable a TOTP device',
        parameters=[
            OpenApiParameter(name='totp_code', type=str)
        ]
    ),
    delete=extend_schema(
        description='Remove a TOTP device',
        parameters=[
            OpenApiParameter(name='totp_code', type=str)
        ]),
)
class TOTPView(APIView):

    def get(self, request):
        device = get_user_totp_device(request.user)
        if not device:
            device = request.user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)

    def post(self, request):
        device = get_user_totp_device(request.user)
        if not device:
            return Response(dict(errors=['You have not setup two factor authentication.']), status=status.HTTP_400_BAD_REQUEST)
        if device.confirmed:
            return Response(dict(errors=['You already have confirmed your device.']), status=status.HTTP_400_BAD_REQUEST)
        if 'totp_code' in request.POST and device.verify_token(request.POST.get('totp_code')):
            device.confirmed = True
            device.save()
            return Response("Device confirmed", status=status.HTTP_200_OK)
        return Response(dict(errors=dict(token=['Invalid TOTP Token.'])), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        device = get_user_totp_device(request.user)
        if not device:
            return Response(dict(errors=['You have not setup two factor authentication.']), status=status.HTTP_400_BAD_REQUEST)
        if not device.confirmed:
            return Response(dict(errors=['Please confirm your device first.']), status=status.HTTP_400_BAD_REQUEST)
        if 'totp_code' in request.POST and device.verify_token(request.POST.get('totp_code')):
            device.delete()
            return Response("Device deleted and 2FA deactivated", status=status.HTTP_204_NO_CONTENT)
        return Response(dict(errors=dict(token=['Invalid TOTP Token.'])), status=status.HTTP_400_BAD_REQUEST)
