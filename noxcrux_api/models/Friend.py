from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Friend(models.Model):

    user = models.ForeignKey(User, models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, models.CASCADE, related_name="reverse_friends")
    created = models.DateTimeField(default=timezone.now)
    validated = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "friend"]

    def __str__(self):
        if self.validated:
            return "User %s is friend with %s" % (self.user, self.friend)
        else:
            return "User %s is waiting to be friend with %s" % (self.user, self.friend)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.user == self.friend:
            raise ValidationError("Users cannot be friend with themselves.")
        super(Friend, self).save(*args, **kwargs)


@receiver(post_delete, sender=Friend)
def delete_friendship(sender, instance, using, **kwargs):
    reverse_friendship = Friend.objects.filter(user=instance.friend, friend=instance.user)
    if reverse_friendship:
        reverse_friendship.delete()
