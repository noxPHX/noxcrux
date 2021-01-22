from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from noxcrux_api.views.OTP import get_user_totp_device
from django.contrib.auth.models import User


class TokenDetail(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        res = super(TokenDetail, self).post(request, *args, **kwargs)
        device = get_user_totp_device(User.objects.get(username=request.POST.get('username')), confirmed=True)
        if device:
            if 'totp_code' in kwargs and device.verify_token(kwargs['totp_code']):
                return res
            else:
                return Response(dict(errors=dict(token=['Invalid TOTP Token'])), status=status.HTTP_400_BAD_REQUEST)
        else:
            return res

    def delete(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
