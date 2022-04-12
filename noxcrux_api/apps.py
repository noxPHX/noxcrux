from django.apps import AppConfig


class NoxcruxAPIConfig(AppConfig):
    name = 'noxcrux_api'

    def ready(self):
        from noxcrux_api.signals import friend
        from noxcrux_api.signals import generator
        from noxcrux_api.signals import keys_container
