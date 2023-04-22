from django.urls import path

from .views import (
    index,
    callback,
    user_top_artists,
    user_recently_played,
    user_top_tracks,
    tracks_by_term,
    artists_by_term,
)


app_name = "app"

urlpatterns = [
    path("", index, name="index"),
    path("callback", callback, name="callback"),
    path("stats/", user_top_tracks, name="home"),
    path("stats/top-artists/<str:term>/", artists_by_term, name="artists_term"),
    path("stats/top-tracks/<str:term>/", tracks_by_term, name="tracks_term"),
    path("stats/top-artists/", user_top_artists, name="artists"),
    path("stats/recently-played/", user_recently_played, name="recently_played"),
]
