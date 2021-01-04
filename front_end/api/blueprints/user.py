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
        top_artists.append({'name': one_artist['name'], 'id': one_artist['id']})


    #top tracks
    top_tracks = []
        #FIXME: use order for now...
    #top albums
    top_albums = []


    top_tracks_raw = sp.current_user_top_tracks(time_range='long_term')['items']

    for one_track in top_tracks_raw:

        #take care of top albums
        one_top_album = {'name': one_track['album']['name'], 'id':one_track['album']['id'], 'artists':[] }
        for one_album_artist in one_track['album']['artists']:
            #one_top_album += one_album_artist['name']
            one_top_album['artists'].append({'name': one_album_artist['name'], 'id': one_album_artist['id']})

        if one_top_album not in top_albums:
            top_albums.append(one_top_album)


        #take care of top tracks
        one_top_track = {'name': one_track['name'], 'id': one_track['id'], 'artists':[] }

        for one_track_artist in one_track['artists']:
            one_top_track['artists'].append({'name': one_track_artist['name'], 'id': one_track_artist['id']})

        top_tracks.append(one_top_track)

    #{user_name, num_followers, user_following_num, country}
    user_info = {'user_name': user_name, 'num_followers': user_num_followers,
                 'user_following_num': user_following_num, 'num_public_playlists': num_public_playlists,
                'num_private_playlists': num_private_playlists,'country': user_country_code,
                'user_saved_songs': user_saved_songs, 'top_artists': top_artists,
                 'top_tracks': top_tracks, 'top_albums': top_albums
                 }

    return render_template('user/dashboard_interface.html', user_name=session['user_name'], user_info=user_info)




@user_bp.route('/artistdetails/<artist_id>')
@login_required
@token_checked
def artist_details(artist_id):
    sp = get_spotify_object()
    artist_details = sp.artist(artist_id)

    return artist_details


@user_bp.route('/trackdetails/<track_id>')
@login_required
@token_checked
def track_details(track_id):
    sp = get_spotify_object()
    track_details = sp.track(track_id)
    return track_details


@user_bp.route('/albumdetails/<album_id>')
@login_required
@token_checked
def album_details(album_id):
    sp = get_spotify_object()
    album_details = sp.album(album_id)
    return album_details


#FIXME:
@user_bp.route('/recentlyplayed')
def recently_played():
    #recently played tracks
    recently_played_tracks = []
    sp = get_spotify_object()
    temp = sp.current_user_recently_played()
    print("---recently played")
    for one_hist in temp['items']:
        print("---one hist")
        track_name = one_hist['track']['name']
        time_played = one_hist['played_at']
        recently_played_tracks.append(track_name)
    #print("total: " + str(len(temp['items'])))
    return temp
