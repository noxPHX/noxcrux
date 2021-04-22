from django.urls import path
from noxcrux_api.views.User import UserList, PasswordUpdate, Profile
from noxcrux_api.views.Horcrux import HorcruxList, HorcruxDetail, HorcruxGrantedList, HorcruxGrant, HorcruxRevoke, HorcruxSearch
from noxcrux_api.views.Token import TokenDetail
from noxcrux_api.views.Generator import GeneratorDetail
from noxcrux_api.views.OTP import TOTPView
from noxcrux_api.views.Friend import FriendList, FriendDestroy, FriendRequestsList, FriendRequestUpdate
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('token/', TokenDetail.as_view()),
    path('totp/', TOTPView.as_view()),
    path('users/', UserList.as_view(), name='users'),
    path('user/me/', Profile.as_view()),
    path('user/password/', PasswordUpdate.as_view()),
    path('horcruxes/', HorcruxList.as_view(), name='horcruxes'),
    path('horcruxes/granted/', HorcruxGrantedList.as_view()),
    path('horcrux/search/<str:name>/', HorcruxSearch.as_view()),
    path('horcrux/shared/<str:name>/', HorcruxGrant.as_view()),
    path('horcrux/shared/<str:name>/<str:username>/', HorcruxRevoke.as_view()),
    path('horcrux/<str:name>/', HorcruxDetail.as_view()),
    path('generator/', GeneratorDetail.as_view(), name='generate'),
    path('friends/', FriendList.as_view()),
    path('friends/requests/', FriendRequestsList.as_view()),
    path('friends/requests/<str:username>/', FriendRequestUpdate.as_view()),
    path('friends/<str:username>/', FriendDestroy.as_view()),
]
