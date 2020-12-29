from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from noxcrux_api.views.User import UserViewSet, GroupViewSet
from noxcrux_api.views.Horcrux import HorcruxList, HorcruxDetail
from noxcrux_api.views.Token import TokenDetail

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/obtain/', obtain_auth_token),
    path('token/revoke/', TokenDetail.as_view()),
    path('horcruxes/', HorcruxList.as_view(), name='horcruxes'),
    path('horcrux/<str:name>/', HorcruxDetail.as_view()),
]
