#api relate to login, logout
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from flask import request, url_for, session, redirect
import spotipy
from front_end.api.decorators import login_required
from front_end.api.extensions import db, db_cursor
from front_end.api.utils import get_spotify_oauth, get_token_info, get_spotify_object, refresh_token_info
from front_end.api.decorators import token_checked

@auth_bp.route('/auth/login')
def login():
    #set up the spotify authorization
    sp_oauth = get_spotify_oauth()

    #make the authorization request and return the like user need to approve the request
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


#FIXME: no idea how to revoke the access token, i will do it with login with the help of session then
@auth_bp.route('/auth/logout')
@login_required
def logout():
    session['logged_in'] = False
    return "logged out successfully"

@auth_bp.route('/auth/accessdenied')
def access_denied():
    return 'access denied'

@auth_bp.route('/test')
@login_required #login_required need to under the route
def test():
    return "login will be required..."


#FIXME: not done, not return if access token is None
@auth_bp.route('/gettracks')
@login_required
def get_tracks():
    print("------reach get tracks")
    try:
        #check if token exist
        token_info = get_token_info()

        #get spotify object that we will make request of
        sp = get_spotify_object()

        return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'][0])
    except Exception as e:
        print(e)
        #return redirect(url_for('main.index'))
        return redirect(url_for('auth.login'))






# the page the spotify will redirect users back after user approve/deny the request
@auth_bp.route('/auth/redirect')
def redirect_page():
    print("--reach redirect page..")
    sp_oauth = get_spotify_oauth()
    session.clear()

    #get the query string pass along with redirct url
    code = request.args.get('code')

    #if not code is given, then user did not approve the request
    if code is None:
        try:
            del session["TOKEN_INFO"]
        finally:
            return 'Authorization failed'

    #get token info with the code passsed back, disable checking cache
    token_info = sp_oauth.get_access_token(code, check_cache=False)

    #save token information into the session
    session["TOKEN_INFO"] = token_info

    #FIXME: refresh the token, I just changed the order of this line
    refresh_token_info(token_info['refresh_token'])



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

            db_cursor.execute(sql_command_search)
            db_result = db_cursor.fetchall()

        cur_user_id = db_result[0][0]
        cur_user_name = db_result[0][1]

        #log user in with the help of sessions
        session['logged_in'] = True
        session['user_id'] = cur_user_id
        session['user_name'] = cur_user_name


    except Exception as e:
        print(e)

    #redirect user to the actual function they are requesting
    #FIXME: for now
    #return redirect(url_for('auth.get_tracks', _external=True))
    return redirect(url_for('user.home', _external=True))


