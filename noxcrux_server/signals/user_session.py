from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from noxcrux_api.models.UserSession import UserSession


@receiver(user_logged_in)
def create_user_session(sender, user, request, **kwargs):
    UserSession.objects.get_or_create(
        user=user,
        session_id=request.session.session_key
    )
