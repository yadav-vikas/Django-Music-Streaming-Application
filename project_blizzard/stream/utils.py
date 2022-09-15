import mutagen
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
import datetime
import random

import re
from django.template.defaultfilters import slugify

# import mutagen.[format]
# metadata = mutagen.[format].Open(filename)
# https://mutagen.readthedocs.io/en/latest/api/base.html


def audio_duration(file):
    """returns the duration of the audio file

    Args:
        file (audio_file): the audio file you want to upload

    Returns:
        datetime.timedelta: timedelta object containing the duration of the audio
    """
    audio_file = mutagen.File(file)
    duration = datetime.timedelta(hours=audio_file.info.length//3600,minutes=audio_file.info.length//60, seconds=audio_file.info.length%60)
    return duration

def audio_stats(file):
    """MPEG audio stream information

    details :

    lenth(Type:float): audio length, in seconds
    Channels(Type:int): number of audio channels
    bitrate(Type:int): audio bitrate, in bits per second. In case bitrate_mode is BitrateMode.UNKNOWN the bitrate is guessed based on the first frame.
    sample_rate(Type:int): audio sample rate, in Hz
    encoder_info(Type:mutagen.text): a string containing encoder name and possibly version. In case a lame tag is present this will start with "LAME ", if unknown it is empty, otherwise the text format is undefined.
    bitrate_mode(Type:bitrate_mode): bitrate_mode
    track_gain(Type:float or None): replaygain track gain (89db) or None
    track_peak(Type:float or None): replaygain track peak or None
    album_gain(Type:float or None): replaygain album gain (89db) or None
    version(Type:float): MPEG version (1, 2, 2.5)
    layer(Type:int): 1, 2, or 3
    mode(Type:int): One of STEREO, JOINTSTEREO, DUALCHANNEL, or MONO (0-3)
    protected(Type:bool): whether or not the file is “protected”
    sketchy(Type:bool): if true, the file may not be valid MPEG audio

    Args:
        file (audio_file): MPEG format file

    Returns:
        dict: details of the audio file
    """
    file_details = {}
    audio_file = mutagen.File(file)
    file_details['basic'] = audio_file.info.pprint()
    file_details.update(audio_file.info.__dict__)
    return file_details

def unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value

def slugify_instance(instance, save=False, new_slug=None, slug_field_name='name'):
    slug_field = instance._meta.get_field(slug_field_name)
    slug = getattr(instance, slug_field.attname)

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.slug)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        rand_int = random.randint(300_000, 500_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance