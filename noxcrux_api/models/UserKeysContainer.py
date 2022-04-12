from django.db import models
from django.contrib.auth.models import User


class UserKeysContainer(models.Model):

    user = models.OneToOneField(User, models.CASCADE)
    public_key = models.CharField(max_length=8192)
    private_key = models.CharField(max_length=8192)
    iv = models.CharField(max_length=255)
