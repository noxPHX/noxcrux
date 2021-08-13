from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class UserSession(models.Model):

    user = models.ForeignKey(User, models.CASCADE)
    session = models.ForeignKey(Session, models.CASCADE)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(null=True, blank=True, max_length=255)
