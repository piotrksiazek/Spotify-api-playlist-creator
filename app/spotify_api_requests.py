from config import CLIENT_ID, CLIENT_SECRET, scope, redirect_uri
from flask import redirect, url_for, request, session, json, Blueprint
import requests
from datetime import datetime

BASE_URL = "https://api.spotify.com/v1/me/"

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
    return make_api_request('playlists')

def get_user_id():
    return make_api_request("")['id']

@spotify_api_requests.route('/create_new_playlist')
def create_new_playlist():
    if can_make_request():
        access_token = session.get("access_token")
        headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + access_token}
        request_body = json.dumps({
            "name": "zło",
            "description": "New playlist description",
            "public": 'false'
        })
        URL = f'https://api.spotify.com/v1/users/{get_user_id()}/playlists'
        response = requests.post(URL, data=request_body, headers=headers)
        return str(response.text)
    return "SD"
    