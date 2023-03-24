from django.urls import path

from .views import index, callback, top_artists, recently_played, home


app_name = "app"

urlpatterns = [
    path("", index, name="index"),
    path("callback", callback, name="callback"),
    path("stats/top-artists/", top_artists, name="top-artists"),
    path("stats/", home, name="home"),
    path("stats/recently-played/", recently_played, name="recently_played"),
]
