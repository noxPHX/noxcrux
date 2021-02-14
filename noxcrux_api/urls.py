from django.urls import path, re_path
from noxcrux_api.views.User import UserList, UserUpdate, PasswordUpdate, Profile
from noxcrux_api.views.Horcrux import HorcruxList, HorcruxDetail
from noxcrux_api.views.Token import TokenDetail
from noxcrux_api.views.Generator import GeneratorDetail
from noxcrux_api.views.OTP import TOTPView
from noxcrux_api.views.Friend import FriendList, FriendRequest

urlpatterns = [
    path(r'token/', TokenDetail.as_view()),
    re_path(r'^token/(?P<totp_code>[0-9]{6})/$', TokenDetail.as_view()),
    path('totp/', TOTPView.as_view()),
    re_path(r'^totp/(?P<totp_code>[0-9]{6})/$', TOTPView.as_view()),
    path('users/', UserList.as_view(), name='users'),
    path('user/me/', Profile.as_view()),
    path('user/username/', UserUpdate.as_view()),
    path('user/password/', PasswordUpdate.as_view()),
    path('horcruxes/', HorcruxList.as_view(), name='horcruxes'),
    path('horcrux/<str:name>/', HorcruxDetail.as_view()),
    path('generator/', GeneratorDetail.as_view(), name='generate'),
    path('friends/', FriendList.as_view()),
    path('friends/requests/', FriendRequest.as_view()),
    path('friends/requests/<str:username>/', FriendRequest.as_view()),
    path('friends/<str:username>/', FriendList.as_view()),
]
