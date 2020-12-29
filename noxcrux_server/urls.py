from django.urls import path
from noxcrux_server.views.Access import LoginView, LogoutView
from noxcrux_server.views.Home import HomeView
from noxcrux_server.views.Horcrux import HorcruxAdd, HorcruxEdit, HorcruxDelete

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', LogoutView.as_view(), name="register"),
    path('', HomeView.as_view(), name="home"),
    path('horcrux/delete/<str:name>/', HorcruxDelete.as_view(), name="horcrux_delete"),
    path('horcrux/edit/<str:name>/', HorcruxEdit.as_view(), name="horcrux_edit"),
    path('horcrux/add/', HorcruxAdd.as_view(), name="horcrux_add"),
]
