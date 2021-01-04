import os
from spotipy.oauth2 import SpotifyOAuth
from flask import url_for, session
import spotipy
from front_end.api.decorators import token_checked

#return spotify oauth object that takes care of the oauth, including access key and refresh key, etc
def get_spotify_oauth():
    sp_oauth = SpotifyOAuth(
        client_id= os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('auth.redirect_page', _external=True),
        #important
        scope="user-library-read, "
              "user-read-email, "
              "user-read-private,"
              "playlist-read-private,"
              "user-read-recently-played,"
              "user-top-read"
    )

    return sp_oauth
"""
sp_oauth = None
def get_spotify_oauth():
    global sp_oauth
    if sp_oauth is None:
        sp_oauth = SpotifyOAuth(
        client_id= os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('auth.redirect_page', _external=True),
        #important
        scope="user-library-read, "
              "user-read-email, "
              "user-read-private,"
              "playlist-read-private,"
              "user-read-recently-played,"
              "user-top-read"
        )

    return sp_oauth
"""


#one spotify object per user
@token_checked
def get_spotify_object():
    token_info = get_token_info()
    sp_object = spotipy.Spotify(auth=token_info['access_token'])
    return sp_object



#refresh the access token
def refresh_token_info(refresh_token):
    sp_oauth_local = get_spotify_oauth()
    session['TOKEN_INFO'] = sp_oauth_local.refresh_access_token(refresh_token)
    print("----------refreashed... session now: ")
    print(session['TOKEN_INFO'])

def get_token_info():
    token_info = session.get("TOKEN_INFO", None)

    if token_info is None:
        return None

    sp_oauth_local = get_spotify_oauth()
    if sp_oauth_local.is_token_expired(token_info):
        session['TOKEN_INFO'] = refresh_token_info(token_info['refresh_token'])

    return session['TOKEN_INFO']
