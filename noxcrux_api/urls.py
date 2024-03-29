from django.urls import path
from noxcrux_api.views.User import UserList, PasswordUpdate, Profile
from noxcrux_api.views.Horcrux import HorcruxList, HorcruxDetail, HorcruxGrantedList, HorcruxGrant, HorcruxRevoke, HorcruxSearch, HorcruxGrantedSearch
from noxcrux_api.views.Token import TokenDetail
from noxcrux_api.views.Generator import GeneratorDetail
from noxcrux_api.views.OTP import TOTPView
from noxcrux_api.views.Friend import FriendList, FriendDestroy, FriendRequestsList, FriendRequestUpdate
from noxcrux_api.views.UserSession import UserSessionList, UserSessionRevoke, UserToken
from noxcrux_api.views.UserKeysContainer import UserPublicKey
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('token/', TokenDetail.as_view(), name='token'),
    path('totp/', TOTPView.as_view(), name='api-totp'),
    path('users/', UserList.as_view(), name='users'),
    path('users/<str:username>/', UserPublicKey.as_view(), name='api-user-pk'),
    path('user/me/', Profile.as_view(), name='api-me'),
    path('user/password/', PasswordUpdate.as_view(), name='api-password'),
    path('user/sessions/', UserSessionList.as_view(), name='api-sessions'),
    path('user/sessions/<str:session>/', UserSessionRevoke.as_view(), name='api-sessions-revoke'),
    path('user/token/', UserToken.as_view(), name='api-sessions-token'),
    path('horcruxes/', HorcruxList.as_view(), name='horcruxes'),
    path('horcruxes/search/<str:search>/', HorcruxSearch.as_view(), name='api-horcruxes-search'),
    path('horcruxes/granted/', HorcruxGrantedList.as_view(), name='api-horcruxes-granted'),
    path('horcruxes/granted/search/<str:search>/', HorcruxGrantedSearch.as_view(), name='api-horcruxes-granted-search'),
    path('horcrux/shared/<str:name>/', HorcruxGrant.as_view(), name='api-horcruxes-grant'),
    path('horcrux/shared/<str:name>/<str:username>/', HorcruxRevoke.as_view(), name='api-horcruxes-granted-revoke'),
    path('horcrux/<str:name>/', HorcruxDetail.as_view(), name='api-horcrux'),
    path('generator/', GeneratorDetail.as_view(), name='generate'),
    path('friends/', FriendList.as_view(), name='api-friends'),
    path('friends/requests/', FriendRequestsList.as_view(), name='api-friends-requests'),
    path('friends/requests/<str:username>/', FriendRequestUpdate.as_view(), name='api-friends-update'),
    path('friends/<str:username>/', FriendDestroy.as_view(), name='api-friend-destroy'),
]
