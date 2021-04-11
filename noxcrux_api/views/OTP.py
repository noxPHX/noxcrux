from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from noxcrux_api.serializers.OTP import TOTPSerializer
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import devices_for_user
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes


def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


@extend_schema_view(
    get=extend_schema(
        description='Set up a new TOTP device, returns the 2FA secret.',
        responses={(200, 'application/json'): OpenApiTypes.STR}
    ),
    put=extend_schema(description='Verify/Enable a TOTP device.'),
    delete=extend_schema(description='Remove a TOTP device.')
)
class TOTPView(RetrieveUpdateDestroyAPIView):
    serializer_class = TOTPSerializer

    def get_object(self):
        return get_user_totp_device(self.request.user)

    def get(self, request, *args, **kwargs):
        device = self.get_object()
        if not device:
            device = request.user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = self.get_serializer(device, data=request.data)
        serializer.is_valid(raise_exception=True)
        if not device.confirmed:
            return Response(dict(errors=['Please confirm your 2FA first.']), status=status.HTTP_400_BAD_REQUEST)
        device.delete()
        return Response("Device deleted and 2FA deactivated", status=status.HTTP_204_NO_CONTENT)
