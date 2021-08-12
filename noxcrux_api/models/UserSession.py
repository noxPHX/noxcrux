from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class UserSession(models.Model):

    user = models.ForeignKey(User, models.CASCADE)
    session = models.ForeignKey(Session, models.CASCADE)
