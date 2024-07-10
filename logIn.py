# File: logIn.py
import requests
import extra_streamlit_components as stx
from urllib.parse import urlencode
import base64
import streamlit as st

# Set up Spotify credentials
CLIENT_ID = '2d5c3f51dca64593a551a89541d6f90a'
CLIENT_SECRET = '361957cb4fee45ca8c5f07289e1c27b0'
REDIRECT_URI = 'http://localhost:8501'  # Ensure this matches exactly with the registered URI

# Initialize cookie manager
cookie_manager = stx.CookieManager()

def generate_random_string(length):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Authentication URL construction
def get_auth_url(state):
    scope = 'user-read-private user-read-email'
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': st.secrets.CLIENT_ID,
        'scope': scope,
        'redirect_uri': st.secrets.REDIRECT_URI,
        'state': state
    })
    return auth_url

# Token request
def get_token(code):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode((st.secrets.CLIENT_ID + ':' + st.secrets.CLIENT_SECRET).encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': st.secrets.REDIRECT_URI
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Refresh token request
def refresh_token(refresh_token):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode((st.secrets.CLIENT_ID + ':' + st.secrets.CLIENT_SECRET).encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()
