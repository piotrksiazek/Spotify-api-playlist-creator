from config import CLIENT_ID, CLIENT_SECRET, scope, redirect_uri
from flask import redirect, url_for, request, session, json, Blueprint
import requests
from datetime import datetime
from Playlist import Playlist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

BASE_URL = "https://api.spotify.com/v1/me/"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
spotify_api_requests = Blueprint('spotify_api_requests', __name__, static_folder="static", template_folder="templates")

def can_make_request():
    if 'access_token' not in session or 'refresh_token' not in session not in session or 'expiration_date' not in session:
        return False
    if datetime.now() > session.get("expiration_date"):
        return False
    return True

def make_api_request(endpoint: str, post_=False, put_=False, params={}) -> str:
    if can_make_request():
        access_token = session.get("access_token")
        headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + access_token}

        if post_:
            requests.post(BASE_URL + endpoint, params, headers=headers)

        if put_:
            requests.put(BASE_URL + endpoint, headers=headers)

        response = requests.get(BASE_URL + endpoint, {}, headers=headers)

        return response.json() if response.status_code == 200 else {"error": "spotify api request failed"}

@spotify_api_requests.route('/get_user_playlists')
def get_user_playlists():
    """
    extract names and ids from user playlylists
    """
    response = []
    items = make_api_request('playlists')['items']
    for item in items:
        playlist = {}
        playlist['name'] = item['name']
        playlist['id'] = item['id']
        playlist['tracks'] = Playlist.get_playlist_items(spotify, item['id'], 'track', unique=False)
        response.append(playlist)
    return json.dumps(response)

@spotify_api_requests.route('/get_playlist_tracks')
def get_playlist_tracks():
    return Playlist.get_playlist_items(spotify, )


def get_user_id():
    return make_api_request("")['id']

def create_new_playlist(name: str, description: str = "New playlist description", is_public: bool = True):
    if can_make_request():
        public = 'true' if is_public else 'false'
        access_token = session.get("access_token")
        headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + access_token}
        request_body = json.dumps({
            "name": name,
            "description": description,
            "public": public
        })
        URL = f'https://api.spotify.com/v1/users/{get_user_id()}/playlists'
        response = requests.post(URL, data=request_body, headers=headers)
        return {'status': response.status_code}
    return {'status': 400}
    