import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
scope = "playlist-modify-public playlist-modify-private"
redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")
