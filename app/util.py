import bs4, requests
import tekore as tk

from django.conf import settings
from django.shortcuts import redirect

client_id = settings.SPOTIFY_CLIENT_ID
client_secret = settings.SPOTIFY_CLIENT_SECRET
redirect_uri = settings.REDIRECT_URI
conf = (client_id, client_secret, redirect_uri)


def top_tracks(request, term):
    refresh_token = request.session.get("refresh_token")

    if refresh_token is None:
        return redirect("/")

    top_track = []
    tkn = tk.refresh_user_token(client_id, client_secret, refresh_token)
    sp = tk.Spotify(tkn)
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
    refresh_token = request.session.get("refresh_token")

    if refresh_token is None:
        return redirect("/")

    top_artist = []
    tkn = tk.refresh_user_token(client_id, client_secret, refresh_token)
    sp = tk.Spotify(tkn)
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
