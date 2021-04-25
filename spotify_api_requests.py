from config import CLIENT_ID, CLIENT_SECRET, scope, redirect_uri
from flask import redirect, url_for, request, session, json
import requests

BASE_URL = "https://api.spotify.com/v1/me/"

def make_api_request(endpoint: str, post_=False, put_=False) -> str:
    access_token = session.get("access_token")
    headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + access_token}

    if post_:
        requests.post(BASE_URL + endpoint, headers=headers)

    if put_:
        requests.put(BASE_URL + endpoint, headers=headers)

    response = requests.get(BASE_URL + endpoint, {}, headers=headers)

    return response.json() if response.status_code == 200 else {"error": "spotify api request failed"}
    