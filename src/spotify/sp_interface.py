
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
        self.test_playlist = "5ULAnTPk479ty7PGEY84AL"

    def search(self, title):
        return self.spotify.search(title, limit = self.limit, type = "track")["tracks"]["items"]

    def get_info(self, track_id):
        return self.spotify.track(track_id)

    def get_playlist(self, playlist_id):
        return self.spotify.playlist(playlist_id)

    def analysis(self, track_id):
        return self.spotify.audio_analysis(track_id)

    def features(self, track_id):
        return self.spotify.audio_features([track_id])

    def get_tracks_from_playlist(self, playlist_id):
        return list(map(lambda t: t["track"]["id"], self.get_playlist(playlist_id)["tracks"]["items"]))

    def get_title(self, uri):
        item_id = uri.split(":")[-1]
        if "track" in uri:
            return self.get_info(item_id)["name"]
        elif "playlist" in uri:
            return self.get_playlist(item_id)["name"]
        return f"uri not set properly: {uri}"


# si = SpotifyInterface()
# spotify:track:74yc92Sz8uASKnWdLmls6w
# spotify:playlist:1YRbXuA7PLZepcqDTal8Cj
# t = si.get_info("74yc92Sz8uASKnWdLmls6w")
# p = si.get_playlist("1YRbXuA7PLZepcqDTal8Cj")
