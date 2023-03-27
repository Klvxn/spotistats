import bs4, requests
import tekore as tk
from time import time
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Artist


client_id = settings.SPOTIFY_CLIENT_ID
client_secret = settings.SPOTIFY_CLIENT_SECRET
redirect_uri = settings.REDIRECT_URI
conf = (client_id, client_secret, redirect_uri)

cred = tk.Credentials(*conf)
auth = tk.UserAuth(cred, tk.scope.every)


# Create your views here.
def index(request):

    if request.method == "POST":
        auth_url = auth.url
        request.session["auth_state"] = auth.state
        return redirect(auth_url)

    return render(request, "spotify_login.html")


def callback(request):
    auth_state = request.session.pop("auth_state", None)

    if not auth_state or auth_state != request.GET.get("state"):
        return redirect("/")

    code = request.GET.get("code")
    state = request.GET.get("state")
    token = auth.request_token(code, state)

    request.session["access_token"] = token.access_token
    request.session["refresh_token"] = token.refresh_token

    return redirect(reverse("app:home"))


def home(request):
    start = time()
    refresh_token = request.session.get("refresh_token")

    if refresh_token is None:
        return redirect("/")

    tkn = tk.refresh_user_token(client_id, client_secret, refresh_token)
    sp = tk.Spotify(tkn)

    top_tracks = []
    sp_range = ["short_term", "medium_term", "long_term"]

    for range in sp_range:
        tracks = []
        top_tracks_response = sp.current_user_top_tracks(limit=10, time_range=range)

        for idx, item in enumerate(top_tracks_response.items, start=1):
            track_info = {
                "idx": idx,
                "name": item.name,
                "image_url": item.album.images[1].url,
                "ext_url": item.external_urls,
                "primary_artist": item.artists[0].name,
            }
            tracks.append(track_info)

        tracks_by_range = {f"{range}_tracks": tracks}
        top_tracks.append(tracks_by_range)

    context = {
        "short_term": top_tracks[0],
        "medium_term": top_tracks[1],
        "long_term": top_tracks[2],
    }
    end = time()
    print(end-start)
    return render(request, "base.html", context)


def top_artists(request):
    start = time()
    refresh_token = request.session.get("refresh_token")

    if refresh_token is None:
        return redirect("/")

    tkn = tk.refresh_user_token(client_id, client_secret, refresh_token)
    sp = tk.Spotify(tkn)

    top_artists = []
    sp_range = ["short_term", "medium_term", "long_term"]
    artists = Artist.objects.all()

    for range in sp_range:
        top_artists_response = sp.current_user_top_artists(limit=10, time_range=range)
        _artists = []
        scrape_artists_monthly_listeners(top_artists_response.items)

        for idx, item in enumerate(top_artists_response.items, start=1):
            artist = artists.filter(artist_id=item.id).first()
            artist_info = {
                "idx": idx,
                "name": item.name,
                "image_url": item.images[0].url,
                "external_url": item.external_urls,
                "monthly_listeners": artist.monthly_listeners,
            }
            _artists.append(artist_info)

        artists_by_range = {f"{range}_artists": _artists}
        top_artists.append(artists_by_range)

    context = {
        "short_term": top_artists[0],
        "medium_term": top_artists[1],
        "long_term": top_artists[2],
    }
    end = time()
    print(end - start)
    return render(request, "top_artists.html", context=context)


def scrape_artists_monthly_listeners(artists):
    for artist in artists:
        response = requests.get(f"https://open.spotify.com/artist/{artist.id}")
        data = bs4.BeautifulSoup(response.content, "html.parser")
        content = data.find_all("meta")[5].get("content")
        value = content.split()[-3]

        try:
            Artist.objects.create(
                artist_id=artist.id,
                monthly_listeners=value,
                stage_name=artist.name
            )
        except IntegrityError:
            pass
    return


def recently_played(request):
    refresh_token = request.session.get("refresh_token")

    if refresh_token is None:
        return redirect("/")

    tkn = tk.refresh_user_token(client_id, client_secret, refresh_token)
    sp = tk.Spotify(tkn)
    response = sp.playback_recently_played(limit=20)
    recent_tracks = []

    for idx, item in enumerate(response.items, start=1):
        track = {
            "idx": idx,
            "name": item.track.name,
            "played_at": item.played_at.ctime,
            "image_url": item.track.album.images[1].url,
            "artist": item.track.artists[0].name,
        }
        recent_tracks.append(track)

    context = {"recently_played": recent_tracks}
    return render(request, "recent_tracks.html", context)
