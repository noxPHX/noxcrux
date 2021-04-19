from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from noxcrux_api.views.OTP import get_user_totp_device
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    post=extend_schema(description='Retrieve authentication token.'),
    delete=extend_schema(description='Remove authentication token.'),
)
class TokenDetail(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        res = super(TokenDetail, self).post(request, *args, **kwargs)
        device = get_user_totp_device(User.objects.get(username=request.POST.get('username')), confirmed=True)
        if device:
            if 'totp_code' in request.POST and device.verify_token(request.POST.get('totp_code')):
                return res
            else:
                return Response(dict(errors=dict(totp_code=['Invalid TOTP Token'])), status=status.HTTP_400_BAD_REQUEST)
        else:
            return res

    def delete(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
