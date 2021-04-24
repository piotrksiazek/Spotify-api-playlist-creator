import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


scope = "playlist-modify-public"
my_uri = 'spotify:playlist:1qBB4GjHyKZYnQclPJfNe0'
user='rbegouu2bjgv6t268sa2dc9hj'
