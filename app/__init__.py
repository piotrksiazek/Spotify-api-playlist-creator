from flask import Flask
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import config
from config import Config
from flask_login import LoginManager
from .spotify_api_requests import spotify_api_requests


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(spotify_api_requests, url_prefix="")

from app import routes, models