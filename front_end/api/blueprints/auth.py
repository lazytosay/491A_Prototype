#api relate to login, logout
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from flask import request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time

#FIXME: test
@auth_bp.route('/login')
def login():

    #set up the spotify authorization
    sp_oauth = create_spotify_oauth()
    #make the authorization request and return the like user need to approve the request
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


#FIXME: not done, not return if access token is None
@auth_bp.route('/gettracks')
def get_tracks():
    try:
        #check if token exist
        token_info = get_token()

        #get spotify object that we will make request of
        sp = spotipy.Spotify(auth=token_info['access_token'])


        return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'][0])
    except Exception as e:
        print(e)
        #return redirect(url_for('main.index'))
        return redirect(url_for('auth.login'))



def get_token():
    token_info = session.get(TOKEN_INFO, None)
    #print("token info: " + token_info)
    if not token_info:
        raise Exception("token not exist")

    #check timestamp
    now = int(time.time())

    #if close to expire, get a new one
    is_expired = token_info['expires_at'] - now < 60

    if(is_expired):
        sp_oauth = create_spotify_oauth()
        #extend the lifetime of the access token with the help of refresh_token
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

TOKEN_INFO = 'TOKEN_INFO'
@auth_bp.route('/redirect')
def redirect_page():
    #the page the spotify will redirect users back after user approve/deny the request
    sp_oauth = create_spotify_oauth()
    session.clear()

    #get the query string pass along with redirct page
    code = request.args.get('code')

    #get access token with the code passsed back
    token_info = sp_oauth.get_access_token(code)

    #save token information into the session
    session[TOKEN_INFO] = token_info

    #redirect user to the actual function they are requesting
    return redirect(url_for('auth.get_tracks', _external=True))


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id= os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('auth.redirect_page', _external=True),
        scope="user-library-read"
    )

