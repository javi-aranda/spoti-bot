import os
from typing import List
from spotify_parser import SpotifyParser
import requests
import logging

logger = logging.getLogger(__name__)

class SpotifyAPI():
    

    def __init__(self):
        self.endpoint = 'https://api.spotify.com/v1/playlists/'+os.environ['SPOTIFY_PLAYLIST_ID']+'/tracks'
        self.api_key = os.environ['SPOTIFY_API_KEY']
    
    def add_tracks(self, track_list: str):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+os.environ['SPOTIFY_API_KEY']
        }
        endpoint = self.endpoint+'?uris='+track_list
        r = requests.post(endpoint, headers=headers)
        r.raise_for_status()
        return r.status_code
