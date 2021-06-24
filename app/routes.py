from flask import render_template, redirect, url_for, request, session, json
from flask_login import current_user, login_user, logout_user, login_required
from app import app, models
from urllib.parse import urlencode
import requests
import spotipy
import spotipy.util as util
from datetime import datetime, timedelta
from config import CLIENT_ID, CLIENT_SECRET, scope, redirect_uri
from .spotify_api_requests import make_api_request, can_make_request, spotify, get_user_id, create_new_playlist, create_and_add_songs, add_prefix
from Playlist import Playlist
from Track import Track
import sys

AUTHORIZE_BASE_URL = 'https://accounts.spotify.com/authorize/?'
TOKEN_BASE_URL = 'https://accounts.spotify.com/api/token'

@app.route('/spotify_callback/')
def spotify_callback():
    try:
        code = request.args.get('code')
        error = request.args.get('error')
    except:
        return "unable to retrieve callback code"

    response = requests.post(TOKEN_BASE_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    print("RESPONSE STATUS CODE: " + response.status_code)
    sys.stdout.flush()
    if response.status_code == 200:
        response = response.json()
        session['access_token'] = response['access_token']
        session['token_type'] = response['token_type']
        session['refresh_token'] = response['refresh_token']
        session['expires_in'] = response['expires_in']

        print(f'|||||||||access_token: {response["access_token"]}')
        sys.stdout.flush()
        print(f'|||||||||token_type: {response["token_type"]}')
        sys.stdout.flush()
        print(f'|||||||||refresh_token: {response["refresh_token"]}')
        sys.stdout.flush()
        print(f'|||||||||expires_in: {response["expires_in"]}')
        sys.stdout.flush()

        session['expiration_date'] = datetime.now() + timedelta(seconds=session['expires_in'])


        if 'error' in response.keys():
            return response['error']
    return redirect(url_for('index'))


@app.route('/authorize')
def authorize():
    url = AUTHORIZE_BASE_URL + urlencode({
        'scope': scope,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'client_id': CLIENT_ID
    })

    if 'access_token' not in session or 'refresh_token' not in session or 'token_create' not in session or 'expiration_date' not in session:
        session.pop('access_token', None)
        session.pop('refresh_token', None)
        session.pop('token_create', None)
        session.pop('spotify_username', None)   
        session.pop('expiration_date', None)     
        return redirect(url)
    
    if datetime.now() > session.get("expiration_date"):
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        payload = {"grant_type":"refresh_token","refresh_token":session.get("refresh_token")}
        response = requests.post(url, headers=headers, data=payload, auth=requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
        
        if response.status_code == 200:
            parsed_response = response.json()
            session['access_token'] = parsed_response['access_token']

        else:
            return redirect(url)

    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if can_make_request():
        if request.method == 'POST':
            seed_genres = []
            name = request.form.get('name') if request.form.get('name') else "New Playlist"
            description = ""
            depth = int(request.form.get('depth'))
            size = int(request.form.get('size'))
            seed_tracks = request.form.getlist('seed')
            if seed_tracks:
                track_ids = Playlist.get_deep_recommendations(spotify, get_user_id(),
                                                          seed_tracks, seed_genres, depth, size)
                track_ids = add_prefix('spotify:track:', track_ids)
                create_and_add_songs(track_ids, name, description, True)
        return render_template('recommendations.html')
    return redirect(url_for('authorize'))

#get least popular track
@app.route('/get_least_popular_track', methods=['GET'])
def get_least_popular_track():
    artist_id = request.args['artist_id']
    track_id = ""
    status = ""
    response = {}
    try:
        response['track_id'] = Track.get_the_least_popular_track_id(spotify, artist_id)
        response['status'] = 200
    except spotipy.exceptions.SpotifyException:
        response['track_id'] = ""
        response['status'] = 400
    finally:
        return response

@app.route('/least_popular_track', methods=['GET'])
def least_popular_track():        
    return render_template('least_popular_track.html')
#end get least popular track

#all about that track
@app.route('/all_about_that_track', methods=['GET'])
def all_about_that_track():
    return render_template("all_about_that_track.html")

@app.route('/get_audio_features', methods=['GET'])
def get_audio_features():
    track_id = request.args['track_id']
    return Track.get_audio_features(spotify, track_id)

@app.route('/get_track_info', methods=['GET'])
def get_track_info():
    track_id = request.args['track_id']
    return Track.get_track_info(spotify, track_id)

@app.route('/get_artist_info', methods=['GET'])
def get_artist_info():
    artist_name = request.args['artist_name']
    return Track.get_artist_info_audiodb(artist_name)
#end all about that track


@app.route('/one_album_one_track', methods=['GET', 'POST'])
def one_album_one_track():
    error = ""
    if can_make_request():
        if request.method == 'POST':
            try:
                name = request.form.get('name') if request.form.get('name') else "New Playlist"
                artist_id = request.form.get('artist_id')
                new_track_list = Playlist.get_random_track_from_each_album(spotify, artist_id)
                print(new_track_list)
                create_and_add_songs(new_track_list, name)
            except:
                error = "Something went wrong, maybe you pasted track id instead of artist id?"

    return render_template('one_album_one_track.html', error=error)

@app.route('/mirror', methods=['GET', 'POST'])
def mirror():
    error = ""
    if can_make_request():
        if request.method == 'POST':
            try:
                name = request.form.get('name') if request.form.get('name') else "New Playlist"
                old_playlist_id = request.form.get('playlist')

                artists_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'artist', unique=True)
                tracks_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'track', unique=False)
                new_track_list = Playlist.get_non_popular_tracks(spotify, artists_from_old_playlist, tracks_from_old_playlist)
                create_and_add_songs(new_track_list, name)
            except:
                error = "something went wrong"
    return render_template('mirror.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)