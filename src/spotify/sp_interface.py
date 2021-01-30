
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .sp_config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

class SpotifyInterface:
    """
    Interface for flask to spotipy
    """

    def __init__(self):
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.limit = 24

    def search(self, title):
        return self.spotify.search(title, limit = self.limit, type = "track")["tracks"]["items"]

    def get_info(self, track_id):
        return self.spotify.track(track_id)

    def analysis(self, track_id):
        return self.spotify.audio_analysis(track_id)

    def features(self, track_id):
        return self.spotify.audio_features([track_id])
