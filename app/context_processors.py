import tekore as tk
from django.conf import settings


client_id = settings.SPOTIFY_CLIENT_ID
client_secret = settings.SPOTIFY_CLIENT_SECRET
redirect_uri = settings.REDIRECT_URI
conf = (client_id, client_secret, redirect_uri)

cred = tk.Credentials(*conf)
auth = tk.UserAuth(cred, tk.scope.every)


def current_user(request):
    refresh_token = request.session["refresh_token"]
    tkn = tk.refresh_user_token(client_id, client_secret, refresh_token)
    sp = tk.Spotify(tkn)
    response = sp.current_user()
    user = {
        "name": response.display_name,
        "image_url": response.images[0].url,
    }
    return user
