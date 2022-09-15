from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from .models import Songs
from .utils import slugify_instance

# @receiver(pre_save, sender=Songs)
# def my_callback(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.song_name_slug = slugify_instance(instance=instance, slug_field_name='song_name')