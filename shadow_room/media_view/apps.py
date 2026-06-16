from django.apps import AppConfig


class MediaViewConfig(AppConfig):
    name = 'media_view'
    def ready(self):
        import media_view.components.fc_navbar