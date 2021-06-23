from flask import Flask
from spotipy.oauth2 import SpotifyOAuth
import config
from config import Config
from flask_login import LoginManager
from .spotify_api_requests import spotify_api_requests
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.register_blueprint(spotify_api_requests, url_prefix="")

from app import routes, models