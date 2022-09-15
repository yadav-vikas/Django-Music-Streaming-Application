from email.policy import default
from django import forms
import datetime

from .models import Song, Playlist

def current_year():
    return datetime.date.today().year

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

class MyForm(forms.ModelForm):
    year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('song_name', 'song_thumbnail', 'song_file', 'song_lyrics', 'song_label')


class SongsCreateUpdateForm(forms.ModelForm):
    song_name = forms.CharField(help_text="Song Name", widget=forms.TextInput, required=True)
    song_thumbnail = forms.ImageField(help_text="Song thumbnail", required=False)
    song_lyrics = forms.FileField(help_text="Song lyrics .txt format", required=False)
    song_file = forms.FileField(help_text="Song file .mp3 or .wav", required=True)
    song_label = forms.CharField(help_text="Song License/Label", widget=forms.Textarea, required=False)

    class Meta:
        model = Song
        fields = ('song_name', 'song_thumbnail', 'song_file', 'song_lyrics', 'song_label')

    def clean(self):
        cleaned_data = super(SongsCreateUpdateForm, self).clean()
        song_name = cleaned_data.get('song_name')
        song_file = cleaned_data.get('song_file')

        if not song_name and not song_file:
            return forms.ValidationError("Please provide song name and file.")

class PlaylistCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, user_id=None, **kwargs):   
        super(PlaylistCreateUpdateForm, self).__init__(*args, **kwargs)
        self.user_id = user_id

    playlist_name = forms.CharField(help_text="Playlist Name", widget=forms.TextInput, required=True)
    playlist_thumbnail = forms.ImageField(help_text="playlist thumbnail", required=False)
    playlist_public_or_private = forms.BooleanField(initial=False, help_text="make your playlist private", required=False)
    
    class Meta:
        model = Playlist
        fields = ('playlist_name', 'playlist_thumbnail', 'playlist_public_or_private')

    def clean(self):
        cleaned_data = super(PlaylistCreateUpdateForm, self).clean()
        playlist_name = cleaned_data.get('playlist_name')

        if not playlist_name:
            return forms.ValidationError("Please provide valid name for playlist.")
