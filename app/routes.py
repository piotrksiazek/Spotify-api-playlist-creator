from flask import render_template, redirect, url_for, request, session, json
from flask_login import current_user, login_user, logout_user, login_required
from app import app, models
from urllib.parse import urlencode
import requests
import spotipy
import spotipy.util as util
from datetime import datetime, timedelta
from config import CLIENT_ID, CLIENT_SECRET, scope, redirect_uri
from .spotify_api_requests import make_api_request, can_make_request

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
    if response.status_code == 200:
        response = response.json()
        session['access_token'] = response['access_token']
        session['token_type'] = response['token_type']
        session['refresh_token'] = response['refresh_token']
        session['expires_in'] = response['expires_in']
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


if __name__ == '__main__':
    app.run(debug=True)
