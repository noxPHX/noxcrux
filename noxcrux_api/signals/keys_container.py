from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from noxcrux_api.models.UserKeysContainer import UserKeysContainer


@receiver(post_save, sender=User)
def create_keys_container(sender, instance, created, **kwargs):
    if created:
        UserKeysContainer.objects.create(user=instance)
