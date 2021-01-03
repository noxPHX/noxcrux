from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from noxcrux_api.views.User import UserList, UserUpdate, PasswordUpdate
from noxcrux_api.views.Horcrux import HorcruxList, HorcruxDetail
from noxcrux_api.views.Token import TokenDetail

urlpatterns = [
    path('token/obtain/', obtain_auth_token),
    path('token/revoke/', TokenDetail.as_view()),
    path('users/', UserList.as_view(), name='users'),
    path('user/<str:username>/', UserUpdate.as_view()),
    path('user/<str:username>/password/', PasswordUpdate.as_view()),
    path('horcruxes/', HorcruxList.as_view(), name='horcruxes'),
    path('horcrux/<str:name>/', HorcruxDetail.as_view()),
]
