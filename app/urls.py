from django.urls import path

from .views import (
    index,
    callback,
    artists,
    recently_played,
    home,
    tracks_by_term,
    artists_by_term,
)


app_name = "app"

urlpatterns = [
    path("", index, name="index"),
    path("callback", callback, name="callback"),
    path("stats/", home, name="home"),
    path("stats/top-artists/<str:term>/", artists_by_term, name="artists_term"),
    path("stats/top-tracks/<str:term>/", tracks_by_term, name="tracks_term"),
    path("stats/top-artists/", artists, name="artists"),
    path("stats/recently-played/", recently_played, name="recently_played"),
]
