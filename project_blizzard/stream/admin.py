from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(Mood)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(ReleasedAlbum)
admin.site.register(ReleasedPlaylist)
admin.site.register(ReleasedMood)
admin.site.register(ReleasedGenre)
admin.site.register(MoodPlaylist)
admin.site.register(GenrePlaylist)
admin.site.register(Subscriptions)
admin.site.register(SongViews)
admin.site.register(SongFeedback)