from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('api/', include('noxcrux_api.urls')),
    path('web/', include('noxcrux_server.urls')),
    path('', lambda request: redirect('login')),
]
