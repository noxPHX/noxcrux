from django.contrib import admin
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.Generator import Generator

# Register your models here.
admin.site.register(Horcrux)
admin.site.register(Generator)
