from django.apps import AppConfig

class FilerImageResizeConfig(AppConfig):
    name = 'filer_image_resize'

    def ready(self):
        import filer_image_resize.signals