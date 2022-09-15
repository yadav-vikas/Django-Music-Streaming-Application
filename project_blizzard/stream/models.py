from django.db import models
from django.contrib.auth import get_user_model
from .utils import audio_duration, unique_slugify, slugify_instance
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify 
from django.shortcuts import reverse

import datetime
import os
import random

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value) 


User = get_user_model()

class Song(models.Model):
    song_name = models.CharField(max_length=250, blank=False)
    song_user = models.ManyToManyField(User, related_name='song_user')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True) # uniqueness
    song_thumbnail = models.ImageField(default='default.jpg', upload_to='song/image/', blank=True, null=True)
    song_duration = models.DurationField(default=datetime.timedelta(), blank=True) # keeping default=0:00:00 in the model
    song_file = models.FileField(upload_to='song/file/')
    song_lyrics = models.FileField(upload_to='song/lyrics/', blank=True, null=True)
    song_label = models.CharField(max_length=100, blank=True, null=True)
    song_likes = models.PositiveBigIntegerField(default=0, blank=True, null=True)
    song_dislikes = models.PositiveBigIntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at =  models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='song_created_user', related_query_name='song_created_user')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='song_updated_user', related_query_name='song_updated_user')


    def save(self, *args, **kwargs):
        rand_int = random.randint(300_000, 500_000) # random
        song_slug = f"{self.song_name}-{rand_int}"
        self.slug = slugify(song_slug)
            
        self.song_duration = audio_duration(self.song_file) # adding audio_duration by reading the upload file
        print(self.song_duration, type(self.song_duration))
        super(Song, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.song_name
    
    def get_absolute_url(self):
        return reverse('song_detail', kwargs={'slug': self.slug})


class Album(models.Model):
    album_name = models.CharField(max_length=250, blank=False)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    album_user = models.ManyToManyField(User, related_name='album_user')
    album_song = models.ManyToManyField(Song, through='ReleasedAlbum' ,related_name='album_song')
    album_description = models.TextField(blank=True, null=True)
    album_release_year = models.IntegerField(help_text='year', default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    album_thumbnail = models.ImageField(default='default.jpg', upload_to='album', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_creator')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='album_updated_user', related_query_name='album_updated_user')
    updated_at =  models.DateTimeField(auto_now=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        rand_int = random.randint(300_000, 500_000) # random
        album_slug = f"{self.album_name}-{rand_int}"
        self.slug = slugify(album_slug)
        super(Album, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.album_name

    def get_absolute_url(self):
        return reverse('song_detail', kwargs={'slug': self.slug})


class Genre(models.Model):
    genre_name = models.CharField(max_length=250, blank=False)
    song = models.ManyToManyField(Song, through='ReleasedGenre' ,related_name='genre_song')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    genre_description = models.TextField(blank=True, null=True)
    genre_thumbnail = models.ImageField(default='default.jpg', upload_to='genre', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at =  models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genre_created_user', related_query_name='genre_created_user')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genre_updated_user', related_query_name='genre_updated_user')

    def save(self, *args, **kwargs):
        rand_int = random.randint(300_000, 500_000) # random
        genre_slug = f"{self.genre_name}-{rand_int}"
        self.slug = slugify(genre_slug)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.genre_name



class Mood(models.Model):
    mood_name = models.CharField(max_length=250, blank=False)
    song = models.ManyToManyField(Song, through='ReleasedMood' ,related_name='mood_song')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    mood_description = models.TextField(blank=True, null=True)
    mood_thumbnail = models.ImageField(default='default.jpg', upload_to='mood', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mood_created_user', related_query_name='mood_created_user')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mood_updated_user', related_query_name='mood_updated_user')
    updated_at =  models.DateTimeField(auto_now=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        rand_int = random.randint(300_000, 500_000) # random
        mood_slug = f"{self.mood_name}-{rand_int}"
        self.slug = slugify(mood_slug)
        super(Mood, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.mood_name

class Playlist(models.Model):
    playlist_name = models.CharField(max_length=220, blank=False)
    song = models.ManyToManyField(Song, through='ReleasedPlaylist' ,related_name='playlist_song')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    playlist_thumbnail = models.ImageField(default='default.jpg', upload_to='playlist', blank=True, null=True)
    playlist_public_or_private = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at =  models.DateTimeField(auto_now=True,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlist_created_user', related_query_name='playlist_created_user')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlist_updated_user', related_query_name='playlist_updated_user')

    def save(self, *args, **kwargs):
        rand_int = random.randint(300_000, 500_000) # random
        playlist_slug = f"{self.playlist_name}-{rand_int}"
        self.slug = slugify(playlist_slug)
        super(Playlist, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.playlist_name

class ReleasedPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.playlist} - {self.song}"

class ReleasedMood(models.Model):
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.mood} - {self.song}"

class MoodPlaylist(models.Model):
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.mood} - {self.playlist}"

class ReleasedGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.genre} - {self.song}"

class GenrePlaylist(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.genre} - {self.playlist}"

class ReleasedAlbum(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [['album', 'song']]

    def __str__(self) -> str:
        return f"{self.album} - {self.song}"



class  Subscriptions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user_channel = models.OneToOneField(User, on_delete=models.CASCADE, help_text='user_subscription', related_name='user_subscription')
    subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True)

    def __str__(self):
        return f"{self.user_channel}"

class SongViews(models.Model):
    song = models.ForeignKey(Song, unique=True, related_name='song_counts', help_text='Number of times this song is played.', on_delete=models.CASCADE)
    total_views = models.BigIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.song} - total views = {self.total_views}"


class SongFeedback(models.Model):
    FEEDBACK_OPTIONS = (
        (None,''),
        ('L', 'Like'),
        ('D', 'Dislike'),
    )
    feedback = models.CharField(max_length=1, choices=FEEDBACK_OPTIONS)
    user = models.ForeignKey(User, related_name='user_feedback', on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='song_feedback', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = [['user', 'song']]
    
    def __str__(self) -> str:
        return f"({self.user} - {self.song}) -> {self.feedback}"