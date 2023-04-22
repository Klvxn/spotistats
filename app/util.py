import bs4, requests
import tekore as tk

from django.shortcuts import redirect
from django.conf import settings


client_id = settings.SPOTIFY_CLIENT_ID
client_secret = settings.SPOTIFY_CLIENT_SECRET
redirect_uri = settings.REDIRECT_URI
conf = (client_id, client_secret, redirect_uri)
scope = "user-top-read user-read-recently-played"
cred = tk.Credentials(*conf)
auth = tk.UserAuth(cred, scope)


def is_valid_token(token):
    try:
        tk.Spotify(token).current_user()
        return token
    except tk.Unauthorised:
        return cred.refresh(token)


def top_tracks(request, term):
    access_token = request.session.get("access_token")

    if access_token is None:
        return redirect("/")

    top_track = []

    token = is_valid_token(access_token)
    sp = tk.Spotify(token)
    sp_response = sp.current_user_top_tracks(limit=10, time_range=term)

    for idx, item in enumerate(sp_response.items, start=1):
        track = {
            "idx": idx,
            "name": item.name,
            "image_url": item.album.images[1].url,
            "ext_url": item.external_urls,
            "primary_artist": item.artists[0].name,
        }
        top_track.append(track)

    range = {
        "short_term": "last 4 weeks",
        "medium_term": "last 6 months",
        "long_term": "all time",
    }

    return top_track, range[term]


def top_artists(request, term):
    access_token = request.session.get("access_token")

    if access_token is None:
        return redirect("/")

    top_artist = []
    token = is_valid_token(access_token)
    sp = tk.Spotify(token)
    sp_response = sp.current_user_top_artists(limit=10, time_range=term)

    for idx, item in enumerate(sp_response.items, start=1):
        artist = {
            "idx": idx,
            "name": item.name,
            "image_url": item.images[0].url,
            "external_url": item.external_urls,
            "monthly_listeners": retrieve_artists_monthly_listeners(item.id)
        }
        top_artist.append(artist)

    range = {
        "short_term": "last 4 weeks",
        "medium_term": "last 6 months",
        "long_term": "all time",
    }

    return top_artist, range[term]


def retrieve_artists_monthly_listeners(artist_id):
    response = requests.get(f"https://open.spotify.com/artist/{artist_id}")
    data = bs4.BeautifulSoup(response.content, "html.parser")
    content = data.find_all("meta")[5].get("content")
    value = content.split()[-3]
    return value


def recently_played(request):
    access_token = request.session.get("access_token")

    if access_token is None:
        return redirect("/")

    token = is_valid_token(access_token)
    sp = tk.Spotify(token)
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

    return recent_tracks
