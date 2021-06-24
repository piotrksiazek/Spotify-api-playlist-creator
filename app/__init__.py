from flask import Flask
from spotipy.oauth2 import SpotifyOAuth
import config
from config import Config
from flask_login import LoginManager
from .spotify_api_requests import spotify_api_requests
from flask_session import Session
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)

app.register_blueprint(spotify_api_requests, url_prefix="")

from app import routes, models