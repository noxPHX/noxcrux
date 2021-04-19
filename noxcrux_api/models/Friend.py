from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Friend(models.Model):

    user = models.ForeignKey(User, models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, models.CASCADE, related_name="reverse_friends")
    created = models.DateTimeField(default=timezone.now)
    validated = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "friend"]

    def __str__(self):
        if self.validated:
            return f"User {self.user} is friend with {self.friend}"
        else:
            return f"User {self.user} is waiting to be friend with {self.friend}"

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.user == self.friend:
            raise ValidationError("Users cannot be friend with themselves.")
        super(Friend, self).save(*args, **kwargs)
