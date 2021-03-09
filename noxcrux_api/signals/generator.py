from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from noxcrux_api.models.Generator import Generator


@receiver(post_save, sender=User)
def create_generator(sender, instance, created, **kwargs):
    if created:
        Generator.objects.create(owner=instance)
