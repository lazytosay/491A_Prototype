#api relate to user specific information
from flask import Blueprint, session, render_template
from front_end.api.utils import get_spotify_object, get_spotify_oauth
from front_end.api.decorators import login_required, token_checked

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/homepage')
@login_required
@token_checked
def home():
    sp = get_spotify_object()

    #----------------------Part One: user profile part------------------------
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


    #Part Two: Top Tracks Part
    """
    #liked songs
    temp = sp.current_user_saved_tracks()
    print("---current user saved tracks..")
    print(temp)
    print("---keys")
    print(temp.keys())
    print(len(temp['items']))
    print("---------one item..")
    for one_item in temp['items']:
        print("--keys")
        print(one_item['track']['name'])
    """

    """
    #recently played tracks
    recently_played_tracks = []
    temp = sp.current_user_recently_played()
    print("---recently played")
    for one_hist in temp['items']:
        print("---one hist")
        track_name = one_hist['track']['name']
        time_played = one_hist['played_at']
        recently_played_tracks.append(track_name)
    print("total: " + str(len(temp['items'])))
    """

    #recently played artists
    top_artists = []
    top_artists_raw = sp.current_user_top_artists(time_range='long_term')['items']

    for one_artist in top_artists_raw:
        top_artists.append(one_artist['name'])


    #top tracks
    top_tracks = []
        #FIXME: use order for now...
    #top albums
    top_albums = []


    top_tracks_raw = sp.current_user_top_tracks(time_range='long_term')['items']

    for one_track in top_tracks_raw:
        cur_album = one_track['album']['name']
        cur_album_artist = one_track['album']['artists'][0]['name']
        temp = cur_album + " -(" + cur_album_artist + ")"
        if temp not in top_albums:
            top_albums.append(temp)
        top_tracks.append(one_track['name'])


    #{user_name, num_followers, user_following_num, country}
    user_info = {'user_name': user_name, 'num_followers': user_num_followers,
                 'user_following_num': user_following_num, 'num_public_playlists': num_public_playlists,
                'num_private_playlists': num_private_playlists,'country': user_country_code,
                'user_saved_songs': user_saved_songs, 'top_artists': top_artists,
                 'top_tracks': top_tracks, 'top_albums': top_albums
                 }

    return render_template('user/dashboard_interface.html', user_name=session['user_name'], user_info=user_info)