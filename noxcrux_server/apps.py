from django.apps import AppConfig


class NoxcruxServerConfig(AppConfig):
    name = 'noxcrux_server'

    def ready(self):
        from noxcrux_api.signals import friend
        from noxcrux_api.signals import generator
