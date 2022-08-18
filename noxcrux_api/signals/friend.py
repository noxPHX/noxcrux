from django.db.models.signals import post_delete
from django.dispatch import receiver
from noxcrux_api.models.Friend import Friend


@receiver(post_delete, sender=Friend)
def delete_friendship(sender, instance, using, **kwargs):
    reverse_friendship = Friend.objects.filter(user=instance.friend, friend=instance.user)
    if reverse_friendship:
        reverse_friendship.delete()

    # Also delete shared horcrux between the two users
    instance.user.shared_horcruxes.filter(horcrux__owner=instance.friend).delete()
    instance.friend.shared_horcruxes.filter(horcrux__owner=instance.user).delete()
