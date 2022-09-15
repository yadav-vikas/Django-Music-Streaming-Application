from re import template
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .forms import PlaylistCreateUpdateForm, SongForm, SongsCreateUpdateForm
from accounts.models import Account

from .models import (
        Album, 
        Song, 
        ReleasedGenre, 
        ReleasedMood,  
        ReleasedAlbum,
        ReleasedPlaylist, 
        Mood, 
        Genre,
        Playlist,
        MoodPlaylist,
        GenrePlaylist,
        Subscriptions, 
    )

import datetime


class SongsListView(ListView):
    model = Song
    template_name = "songs/songs_list.html"
    context_object_name = 'songs_list'
    ordering = ['-id']
    # paginate_by = 10
    
    def get_queryset(self, *args, **kwargs):
        qs = super(SongsListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs

class SongsDetailView(DetailView):
    model = Song
    template_name = "songs/songs_detail.html"
    context_object_name = 'song_name'

    
    def get_queryset(self, *args, **kwargs):
        # qs = super(SongsDetailView, self).get_queryset(*args, **kwargs)
        print("kwards :",self.kwargs.get('slug'))
        query = Song.objects.filter(slug=self.kwargs['slug'])
        # qs = Songs.objects.filter(song_name_slug=query)
        return query

class SongCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Song
    form_class = SongsCreateUpdateForm
    context_object_name = "songs"
    template_name = "songs/new_song.html"
    success_url = reverse_lazy('song_list')
    success_message = "Song %(song_name)s created successfully."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super(SongCreateView, self).form_valid(form)

class SongUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Song
    context_object_name = "songs"
    template_name = "songs/update_song.html"
    form_class = SongsCreateUpdateForm
    success_url = reverse_lazy('song_list')
    success_message = "Song %(song_name)s updated successfully."

    def form_valid(self, form):
        # form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super(SongUpdateView, self).form_valid(form)

class SongDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Song
    context_object_name = "songs"
    template_name = "songs/update_song.html"
    fields = ('song_name', 'song_thumbnail', 'song_file', 'song_lyrics', 'song_license')
    success_url = 'song_list'
    success_message = "Song %(song_name)s deleted successfully."

# class SongsView(View):
#     model = Song
#     form_class = SongForm
#     template_name = "songs/new_song.html"

#     ordering = ['-id']

#     # def get_queryset(self, *args, **kwargs):
#     #     qs = super(SongsList, self).get_queryset(*args, **kwargs)
#     #     qs = qs.order_by("-id")
#     #     return qs

#     def get(self, request, *args, **kwargs):
#         song_list = Song.objects.all()
#         return render(request, self.template_name, {'songs_list': song_list})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return redirect('song_list')

#         return render(request, self.template_name, {'form': form})

class AlbumListView(ListView):
    model = Album
    template_name = "album/album_list.html"
    context_object_name = 'album_list'
    ordering = ['-id']
    # paginate_by = 10
    
    def get_queryset(self, *args, **kwargs):
        qs = super(AlbumListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs

class AlbumDetailView(DetailView):
    model = ReleasedAlbum
    template_name = "album/album_detail.html"
    context_object_name = 'album_name'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        query = get_object_or_404(Album, slug=slug)
        try:
           object = ReleasedAlbum.objects.prefetch_related('album').filter(album=query)
        except ReleasedAlbum.DoesNotExist:
            object = ReleasedAlbum.objects.none()
        except ReleasedAlbum.MultipleObjectsReturned:
            object = ReleasedAlbum.objects.prefetch_related('album').filter(album=query).first()
            #select the apt object
        print("object: ",object)
        return object

class PlaylistListView(ListView):
    model = Playlist
    template_name = "playlist/playlist_list.html"
    context_object_name = 'playlist_list'
    ordering = ['-id']
    # paginate_by = 10
    
    def get_queryset(self, *args, **kwargs):
        qs = super(PlaylistListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs

class PlaylistDetailView(DetailView):
    model = ReleasedPlaylist
    template_name = "playlist/list.html"
    context_object_name = 'playlist_name'

    # def get_object(self, queryset=None):
    #     slug = self.kwargs['slug']
    #     query = get_object_or_404(Playlist, slug=slug)
    #     try:
    #        object = ReleasedPlaylist.objects.prefetch_related('playlist').filter(playlist=query)
    #     except ReleasedPlaylist.DoesNotExist:
    #         object = ReleasedPlaylist.objects.none()
    #     except ReleasedPlaylist.MultipleObjectsReturned:
    #         object = ReleasedPlaylist.objects.prefetch_related('playlist').filter(playlist=query).first()
    #         #select the apt object
    #     print("object: ",object)
    #     return object

    def get_object(self, queryset=None):
        context = {}
        slug = self.kwargs['slug']
        query = get_object_or_404(Playlist, slug=slug)
        try:
            context['playlist'] = ReleasedPlaylist.objects.select_related('playlist').filter(playlist=query).values('playlist__playlist_thumbnail', 'playlist__playlist_name', 'song__song_duration')
            total_duration = datetime.timedelta()
            for duration in context['playlist']:
                total_duration += duration['song__song_duration']
            context['total_duration'] = str(total_duration)
        except ReleasedPlaylist.DoesNotExist:
            context['playlist'] = ReleasedPlaylist.objects.none()
        except ReleasedPlaylist.MultipleObjectsReturned:
            context['playlist'] = ReleasedPlaylist.objects.select_related('playlist').filter(playlist=query).first()
            #select the apt object
        try:
           context['songs'] = ReleasedPlaylist.objects.select_related('song').filter(playlist=query).values('song__song_name', 'song__song_duration', 'song__song_file', 'song__song_thumbnail')
        except ReleasedPlaylist.DoesNotExist:
            context['songs'] = ReleasedPlaylist.objects.none()
        except ReleasedPlaylist.MultipleObjectsReturned:
            context['songs'] = ReleasedPlaylist.objects.select_related('song').filter(playlist=query).first()
            #select the apt object
        print("playlist context :", context)
        return context

class PlaylistCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Playlist
    form_class = PlaylistCreateUpdateForm
    context_object_name = "playlist"
    template_name = "playlist/new_playlist.html"
    success_url = reverse_lazy('playlist_list')
    success_message = "Playlist %(playlist_name)s created successfully."

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(PlaylistCreateView, self).get_form_kwargs()
    #     print("form kwargs :",kwargs)
    #     kwargs['user_id'] = self.request.user.pk
    #     return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super(PlaylistCreateView, self).form_valid(form)


class PlaylistUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Playlist
    context_object_name = "playlist"
    template_name = "playlist/update_playlist.html"
    form_class = PlaylistCreateUpdateForm
    success_url = reverse_lazy('playlist_list')
    success_message = "Playlist %(playlist_name)s updated successfully."

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super(PlaylistUpdateView, self).form_valid(form)

class PlaylistDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Playlist
    context_object_name = "playlist"
    template_name = "playlist/playlist_delete.html"
    fields = ('playlist_name', 'playlist_thumbnail', 'playlist_public_or_private')
    success_url = 'playlist_list'
    success_message = "Playlist %(playlist_name)s deleted successfully."

class MoodListView(ListView):
    model = Mood
    template_name = "mood/mood_list.html"
    context_object_name = 'mood_list'
    ordering = ['-id']
    # paginate_by = 10
    
    def get_queryset(self, *args, **kwargs):
        qs = super(MoodListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs

class MoodDetailView(DetailView):
    model = ReleasedMood
    template_name = "mood/mood_detail.html"
    context_object_name = 'mood_songs'

    def get_object(self, queryset=None):
        context = {}
        slug = self.kwargs['slug']
        query = get_object_or_404(Mood, slug=slug)
        try:
           context['songs'] = ReleasedMood.objects.prefetch_related('mood').filter(mood=query)
        except ReleasedMood.DoesNotExist:
            context['songs'] = ReleasedMood.objects.none()
        except ReleasedMood.MultipleObjectsReturned:
            context['songs'] = ReleasedMood.objects.prefetch_related('mood').filter(mood=query).first()
        try:
           context['playlists'] = MoodPlaylist.objects.prefetch_related('mood').filter(mood=query)
        except MoodPlaylist.DoesNotExist:
            context['playlists'] = MoodPlaylist.objects.none()
        except MoodPlaylist.MultipleObjectsReturned:
            context['playlists'] =  MoodPlaylist.objects.prefetch_related('mood').filter(mood=query).first()
        print("context: ", context)
        return context


# class MoodPlaylistDetailView(DetailView):
#     model = MoodPlaylist
#     template_name = "mood/mood_detail.html"
#     context_object_name = 'mood_playlists'

#     def get_object(self, queryset=None):
#         slug = self.kwargs['slug']
#         print("slug: ",slug)
#         query = get_object_or_404(Mood, slug=slug)
#         print("query: ",query)
#         try:
#            object = MoodPlaylist.objects.prefetch_related('mood').filter(mood=query)
#         except MoodPlaylist.DoesNotExist:
#             object = None
#         except MoodPlaylist.MultipleObjectsReturned:
#             object.first()
#             #select the apt object
#         print("object: ",object)
#         return object

class GenreListView(ListView):
    model = Genre
    template_name = "genre/genre_list.html"
    context_object_name = 'genre_list'
    ordering = ['-id']
    # paginate_by = 10
    
    def get_queryset(self, *args, **kwargs):
        qs = super(GenreListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs

class GenreDetailView(DetailView):
    model = ReleasedGenre
    template_name = "genre/genre_detail.html"
    context_object_name = 'genre_songs'

    def get_object(self, queryset=None):
        context = {}
        slug = self.kwargs['slug']
        query = get_object_or_404(Genre, slug=slug)
        try:
           context['songs'] = ReleasedGenre.objects.prefetch_related('genre').filter(genre=query)
        except ReleasedGenre.DoesNotExist:
            context['songs'] = ReleasedGenre.objects.none()
        except ReleasedGenre.MultipleObjectsReturned:
            context['songs'] = ReleasedGenre.objects.prefetch_related('genre').filter(genre=query).first()
        try:
           context['playlists'] = GenrePlaylist.objects.prefetch_related('genre').filter(genre=query)
        except GenrePlaylist.DoesNotExist:
            context['playlists'] = GenrePlaylist.objects.none()
        except GenrePlaylist.MultipleObjectsReturned:
            context['playlists'] = GenrePlaylist.objects.prefetch_related('genre').filter(genre=query).first()
        print("context: ", context)
        return context

def homes(request):
    return render(request, "stream/homes.html")