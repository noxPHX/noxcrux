from django.db.models.signals import post_delete
from django.dispatch import receiver
from noxcrux_api.models.Friend import Friend


@receiver(post_delete, sender=Friend)
def delete_friendship(sender, instance, using, **kwargs):
    reverse_friendship = Friend.objects.filter(user=instance.friend, friend=instance.user)
    if reverse_friendship:
        reverse_friendship.delete()

    # Also delete shared horcrux between the two users
    [horcrux.grantees.remove(instance.user) for horcrux in instance.user.shared_horcruxes.filter(owner=instance.friend)]
    [horcrux.grantees.remove(instance.friend) for horcrux in instance.friend.shared_horcruxes.filter(owner=instance.user)]
