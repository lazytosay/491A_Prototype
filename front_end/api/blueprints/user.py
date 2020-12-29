#api relate to user specific information
from flask import Blueprint, session, render_template
from front_end.api.utils import get_spotify_object, get_spotify_oauth
from front_end.api.decorators import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/homepage')
@login_required
def home():
    sp = get_spotify_object()
    current_user = sp.current_user()
    print("----------current user")
    print(current_user)


    user_country_code = current_user['country']

    user_name = current_user['display_name']

    user_num_followers = current_user['followers']['total']

    user_id = current_user['id']

    user_email = current_user['email']

    user_following_num = 0
    user_saved_songs = 0

    num_public_playlists = 0
    num_private_playlists= 0


    all_playlists = sp.current_user_playlists(limit=50, offset=0)

    print("---all playlists count")
    print(all_playlists['total'])

    for one_playlist in all_playlists['items']:
        owner_id = one_playlist['owner']['id']

        if owner_id == user_id:
            is_public = one_playlist['public']
            if is_public:
                num_public_playlists += 1
            else:
                num_private_playlists += 1

        else:
            user_following_num += 1

        songs_count = one_playlist['tracks']['total']
        user_saved_songs += songs_count

    #{user_name, num_followers, user_following_num, country}
    user_info = {'user_name': user_name, 'num_followers': user_num_followers,
                 'user_following_num': user_following_num, 'num_public_playlists': num_public_playlists,
                'num_private_playlists': num_private_playlists,'country': user_country_code,
                'user_saved_songs': user_saved_songs
                 }

    return render_template('user/dashboard_interface.html', user_name=session['user_name'], user_info=user_info)