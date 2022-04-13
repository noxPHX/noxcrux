from django.db import models
from django.contrib.auth.models import User


class Horcrux(models.Model):
    site = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    horcrux = models.CharField(max_length=255)
    grantees = models.ManyToManyField(User, related_name='shared_horcruxes')

    class Meta:
        unique_together = ['name', 'owner']

    def __str__(self):
        return self.name
