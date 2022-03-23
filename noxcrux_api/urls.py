from django.urls import path
from noxcrux_api.views.User import UserList, PasswordUpdate, Profile
from noxcrux_api.views.Horcrux import HorcruxList, HorcruxDetail, HorcruxGrantedList, HorcruxGrant, HorcruxRevoke, HorcruxSearch, HorcruxGrantedSearch
from noxcrux_api.views.Token import TokenDetail
from noxcrux_api.views.Generator import GeneratorDetail
from noxcrux_api.views.OTP import TOTPView
from noxcrux_api.views.Friend import FriendList, FriendDestroy, FriendRequestsList, FriendRequestUpdate
from noxcrux_api.views.UserSession import UserSessionList, UserSessionRevoke, UserToken
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('token/', TokenDetail.as_view(), name='token'),
    path('totp/', TOTPView.as_view(), name='api-totp'),
    path('users/', UserList.as_view(), name='users'),
    path('user/me/', Profile.as_view(), name='api-me'),
    path('user/password/', PasswordUpdate.as_view(), name='api-password'),
    path('user/sessions/', UserSessionList.as_view(), name='api-sessions'),
    path('user/sessions/<str:session>/', UserSessionRevoke.as_view(), name='api-sessions-revoke'),
    path('user/token/', UserToken.as_view(), name='api-sessions-token'),
    path('horcruxes/', HorcruxList.as_view(), name='horcruxes'),
    path('horcruxes/search/<str:search>/', HorcruxSearch.as_view()),
    path('horcruxes/granted/', HorcruxGrantedList.as_view()),
    path('horcruxes/granted/search/<str:search>/', HorcruxGrantedSearch.as_view()),
    path('horcrux/shared/<str:name>/', HorcruxGrant.as_view()),
    path('horcrux/shared/<str:name>/<str:username>/', HorcruxRevoke.as_view()),
    path('horcrux/<str:name>/', HorcruxDetail.as_view()),
    path('generator/', GeneratorDetail.as_view(), name='generate'),
    path('friends/', FriendList.as_view()),
    path('friends/requests/', FriendRequestsList.as_view()),
    path('friends/requests/<str:username>/', FriendRequestUpdate.as_view()),
    path('friends/<str:username>/', FriendDestroy.as_view()),
]
