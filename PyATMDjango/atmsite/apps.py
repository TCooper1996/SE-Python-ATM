from django.apps import AppConfig


class AtmsiteConfig(AppConfig):
    name = 'atmsite'

    def ready(self):
        from . import signals