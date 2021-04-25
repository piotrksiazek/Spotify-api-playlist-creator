from flask import Flask
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import config
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

from app import routes, models