from django.db.models.signals import pre_save
from django.dispatch import receiver
from filer.models import Image
from PIL import Image as pil
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings


@receiver(pre_save, sender=Image)
def filer_signal_pre(sender, instance, **kwargs):
    """ Zmenseni obrazku Django-Filer
    """
    SIZES = getattr(settings, 'FILER_IMAGE_RESIZE', (1800, 1200))

    img = instance.file.file
    im = pil.open(img)

    if im.height > SIZES[1] * 1.5:

        output = BytesIO()
        im.thumbnail(SIZES, pil.ANTIALIAS)
        im.save(output, format=im.format, quality=80)
        output.seek(0)

        # uprava filer.models.imagemodels.Image.file.file
        instance.file.file = InMemoryUploadedFile(
            output,
            img.field_name,
            img.name,
            img.content_type,
            im.__sizeof__(),
            None
        )

        # uprava hodnot filer.models.imagemodels.Image
        instance._width = im.width
        instance._height = im.height
        instance._file_size = im.__sizeof__()
    return