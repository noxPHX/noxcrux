from django.contrib import admin
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.Generator import Generator
from noxcrux_api.models.Friend import Friend
from noxcrux_api.models.UserSession import UserSession

# Register your models here.
admin.site.register(Horcrux)
admin.site.register(Generator)
admin.site.register(Friend)
admin.site.register(UserSession)
