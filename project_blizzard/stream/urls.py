from django.urls import path
from .views import (
    SongsListView, SongsDetailView, SongUpdateView, SongsDetailView, SongCreateView, SongDeleteView,
    AlbumListView, AlbumDetailView,
    PlaylistListView, PlaylistDetailView, PlaylistCreateView, PlaylistUpdateView, PlaylistDeleteView,
    MoodListView, MoodDetailView,
    GenreListView, GenreDetailView,
    homes,
)

urlpatterns = [
    path('homes/', homes, name="homes"),
    path('', SongsListView.as_view(), name='song_list'),
    path('song/create/', SongCreateView.as_view(), name='song_create'),
    path('song/update/<slug:slug>/', SongUpdateView.as_view(), name='song_update'),
    path('song/delete/<slug:slug>/', SongDeleteView.as_view(), name='song_delete'),
    path('song/<slug:slug>/', SongsDetailView.as_view(), name='song_detail'),

    path('albums/', AlbumListView.as_view(), name='album_list'),
    path('albums/<slug:slug>/', AlbumDetailView.as_view(), name='album_detail'),
    
    path('playlist/create/', PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlist/', PlaylistListView.as_view(), name='playlist_list'),
    path('playlist/update/<slug:slug>/', PlaylistUpdateView.as_view(), name='playlist_update'),
    path('playlist/delete/<slug:slug>/', PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('playlist/<slug:slug>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    
    path('mood/', MoodListView.as_view(), name='mood_list'),
    path('mood/<slug:slug>/', MoodDetailView.as_view(), name='mood_detail'),
    
    path('genre/', GenreListView.as_view(), name='genre_list'),
    path('genre/<slug:slug>/', GenreDetailView.as_view(), name='genre_detail'),

]