from django.db import models
from django.contrib.auth.models import User
from noxcrux_api.models.Horcrux import Horcrux


class SharedHorcrux(models.Model):

    horcrux = models.ForeignKey(Horcrux, on_delete=models.CASCADE)
    grantee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_horcruxes')
    shared_horcrux = models.CharField(max_length=8192)

    def __str__(self):
        return f"[{str(self.horcrux.owner)}] {str(self.horcrux)}"
