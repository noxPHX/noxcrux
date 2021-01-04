from django.urls import path
from noxcrux_server.views.Access import LoginView, LogoutView, RegisterView
from noxcrux_server.views.Home import HomeView
from noxcrux_server.views.Horcrux import HorcruxAdd, HorcruxEdit, HorcruxDelete
from noxcrux_server.views.User import ProfileView, UsernameUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('', HomeView.as_view(), name="home"),
    path('horcrux/add/', HorcruxAdd.as_view(), name="horcrux_add"),
    path('horcrux/edit/<str:name>/', HorcruxEdit.as_view(), name="horcrux_edit"),
    path('horcrux/delete/<str:name>/', HorcruxDelete.as_view(), name="horcrux_delete"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/username/', UsernameUpdateView.as_view(), name="edit_username"),
]
