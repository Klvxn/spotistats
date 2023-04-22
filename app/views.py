from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponse
from django.template.loader import render_to_string

from .util import auth, top_artists, top_tracks, recently_played


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


def user_top_tracks(request):
    tracks, range = top_tracks(request, "short_term")
    context = {"items": tracks, "term": range}
    return render(request, "base.html", context)


def tracks_by_term(request, term):
    tracks, range = top_tracks(request, term)
    context = {"items": tracks, "term": range}
    response = render_to_string("user_top_tracks.html", context)
    return HttpResponse(response)


def artists_by_term(request, term):
    artist, range = top_artists(request, term)
    context = {"items": artist, "term": range}
    response = render_to_string("user_top_artists.html", context)
    return HttpResponse(response)


def user_top_artists(request):
    artist, range = top_artists(request, "short_term")
    context = {"items": artist, "term": range}
    return render(request, "top_artists.html", context=context)


def user_recently_played(request):
    recent_tracks = recently_played(request)
    context = {"recently_played": recent_tracks}
    return render(request, "recent_tracks.html", context)
