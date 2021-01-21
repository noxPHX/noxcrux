from django.db import models
from django.contrib.auth.models import User
import string
import random

ALLOWED_SYMBOLS = '!@#$%^&*'


class Generator(models.Model):
    upper = models.BooleanField(default=True)
    numeric = models.BooleanField(default=True)
    symbol = models.BooleanField(default=True)
    size = models.IntegerField(default=5)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def generate(self):
        """
        Generate a random horcrux based on the user's preferences
        """
        candidates = string.ascii_lowercase
        if self.upper:
            candidates += string.ascii_uppercase
        if self.numeric:
            candidates += string.digits
        if self.symbol:
            candidates += ALLOWED_SYMBOLS
        return ''.join(random.SystemRandom().choice(candidates) for _ in range(self.size))

    def __str__(self):
        return str(self.owner)
