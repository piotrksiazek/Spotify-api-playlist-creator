from flask import render_template, redirect, url_for, request, session, json
from flask_login import current_user, login_user, logout_user, login_required
from app import app, models
from urllib.parse import urlencode
import requests
import spotipy
import spotipy.util as util


scope = "playlist-modify-public"
redirect_uri = 'http://127.0.0.1:5000/spotify_callback/'

@app.route('/spotify_callback/')
def spotify_callback():
    code = request.args.get('code')
    error = request.args.get('error')

    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    if response.status_code == 200:
        response = response.json()
        session['access_token'] = response['access_token']
        session['token_type'] = response['token_type']
        session['refresh_token'] = response['refresh_token']
        session['expires_in'] = response['expires_in']
        if 'error' in response.keys():
            return response['error']
    return redirect(url_for('index'))

    # access_token = 

@app.route('/authorize')
def authorize():
    url = 'https://accounts.spotify.com/authorize/?' + urlencode({
        'scope': scope,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'client_id': CLIENT_ID
    })
    return redirect(url)

@app.route('/')
def index():
    # sess_access_token, sess_refresh_token, sess_token_create_time = session.get("access_token", None) , session.get('refresh_token', None), session.get('token_create', None)
    # print(sess_access_token)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
