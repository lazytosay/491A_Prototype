#api relate to login, logout
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from flask import request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
#from flask_login import login_user, login_required, current_user, logout_user
from front_end.api.decorators import login_required
from front_end.api.extensions import db, db_cursor

#FIXME: test
@auth_bp.route('/login')
def login():

    #set up the spotify authorization
    sp_oauth = create_spotify_oauth()

    #make the authorization request and return the like user need to approve the request
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


#FIXME: no idea how to revoke the access token, i will do it with login_manager then
@auth_bp.route('/logout')
def logout():
    session['logged_in'] = False
    return "logged out successfully"

@auth_bp.route('/accessdenied')
def access_denied():
    return 'access denied'

@auth_bp.route('/test')
@login_required #login_required need to under the route
def test():
    return "login will be required..."


#FIXME: not done, not return if access token is None
@auth_bp.route('/gettracks')
def get_tracks():
    try:
        #check if token exist
        token_info = get_token_info()

        #get spotify object that we will make request of
        sp = spotipy.Spotify(auth=token_info['access_token'])

        #print("----current users")
        #print(sp.current_user()['display_name'])

        return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'][0])
    except Exception as e:
        print(e)
        #return redirect(url_for('main.index'))
        return redirect(url_for('auth.login'))



def get_token_info():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("token not exist")

    #check timestamp
    now = int(time.time())

    #if close to expire, get a new one
    is_expired = token_info['expires_at'] - now <= 0

    if(is_expired):
        raise Exception("access token expired")
    """
    else:
        sp_oauth = create_spotify_oauth()
        #extend the lifetime of the access token with the help of refresh_token
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    """

    return token_info

TOKEN_INFO = 'TOKEN_INFO'


# the page the spotify will redirect users back after user approve/deny the request
@auth_bp.route('/redirect')
def redirect_page():
    sp_oauth = create_spotify_oauth()
    session.clear()

    #get the query string pass along with redirct url
    code = request.args.get('code')

    if code is None:
        try:
            del session[TOKEN_INFO]
        finally:
            return 'Authorization failed'

    #get token info with the code passsed back
    token_info = sp_oauth.get_access_token(code)

    print("---token info got: ")
    print(token_info)

    #save token information into the session
    session[TOKEN_INFO] = token_info

    #try to log user in
    try:
        # get spotify object that we will make request of
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_name = sp.current_user()['display_name']

        #check if the user already in our database
        sql_command_search = """
            select regular_user_id, user_name 
            from regularusers 
            where user_name = '%s'
            """ %(user_name)

        db_cursor.execute(sql_command_search)
        db_result = db_cursor.fetchall()
        print("--first db result")
        print(db_result)


        # if the user not in our database, create one with its spotify display name
        if len(db_result) == 0:
            sql_command_insert = """
                insert into regularusers(
                    user_name
                    ) values(
                    '%s'
                    )
            """ %(user_name)
            db_cursor.execute(sql_command_insert)
            db.commit()
            print("--inserted")

            db_cursor.execute(sql_command_search)
            db_result = db_cursor.fetchall()

        cur_user_id = db_result[0][0]
        cur_user_name = db_result[0][1]
        print("--cur user name: ")
        print(cur_user_name)

        print("trying to log in..")
        #FIXME: looks like we need a user object
        #login_user(cur_user_id)
        #print("----user logged in")

        #log user in with the help of sessions
        session['logged_in'] = True
        session['user_id'] = cur_user_id
        session['user_name'] = cur_user_name


    except Exception as e:
        print("error here..")
        print(e)

    #redirect user to the actual function they are requesting
    return redirect(url_for('auth.get_tracks', _external=True))


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id= os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('auth.redirect_page', _external=True),
        scope="user-library-read"
    )

