from django.urls import path
from noxcrux_server.views.Access import LoginView, LogoutView, RegisterView
from noxcrux_server.views.Home import HomeView
from noxcrux_server.views.Horcrux import HorcruxAdd, HorcruxEdit, HorcruxDelete, HorcruxShare, HorcruxUnshare
from noxcrux_server.views.User import ProfileView, UsernameUpdateView, PasswordUpdateView, DeleteAccountView
from noxcrux_server.views.Generator import Generator
from noxcrux_server.views.OTP import TOTPLoginView, TOTPMainView, TOTPSecretView, TOTPConfirmView, TOTPDeleteView
from noxcrux_server.views.Friends import FriendsView, FriendDelete, FriendRequestAccept, FriendRequestDelete, FriendAdd

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('login/totp/', TOTPLoginView.as_view(), name="totp"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('', HomeView.as_view(), name="home"),
    path('horcrux/add/', HorcruxAdd.as_view(), name="horcrux_add"),
    path('horcrux/edit/<str:name>/', HorcruxEdit.as_view(), name="horcrux_edit"),
    path('horcrux/delete/<str:name>/', HorcruxDelete.as_view(), name="horcrux_delete"),
    path('horcrux/share/<str:name>/', HorcruxShare.as_view(), name="horcrux_share"),
    path('horcrux/unshare/<str:name>/<str:username>/', HorcruxUnshare.as_view(), name="horcrux_unshare"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/username/', UsernameUpdateView.as_view(), name="edit_username"),
    path('profile/password/', PasswordUpdateView.as_view(), name="edit_password"),
    path('profile/delete/', DeleteAccountView.as_view(), name="delete_account"),
    path('profile/2FA/', TOTPMainView.as_view(), name="2FA"),
    path('profile/2FA/secret/', TOTPSecretView.as_view(), name="2FA_secret"),
    path('profile/2FA/confirm/', TOTPConfirmView.as_view(), name="2FA_confirm"),
    path('profile/2FA/delete/', TOTPDeleteView.as_view(), name="2FA_delete"),
    path('generator/', Generator.as_view(), name="generator"),
    path('friends/', FriendsView.as_view(), name="friend_list"),
    path('friends/add/', FriendAdd.as_view(), name="friend_add"),
    path('friends/delete/<str:username>/', FriendDelete.as_view(), name="friend_delete"),
    path('friends/request/accept/<str:username>/', FriendRequestAccept.as_view(), name="friend_request_accept"),
    path('friends/request/delete/<str:username>/', FriendRequestDelete.as_view(), name="friend_request_delete"),
]
