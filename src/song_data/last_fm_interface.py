
import requests
import pandas as pd

from .last_fm_config import LAST_FM_API_KEY

class LastFMInterface:
    """
    docstring for SpotALike.
    """

    def __init__(self):
        self.base_url = "https://ws.audioscrobbler.com/2.0/"
        self.main_format = "json"
        self.headers = {
            "user-agent": "Musical Fact sheet"
        }

    def build_url(self, track, artist, method, format):
        return f"{self.base_url}?method={method}&api_key={LAST_FM_API_KEY}&artist={artist}&track={track}&format={format}".replace(" ", "%20")

    def get(self, track, artist, method="track.getSimilar", format=None):
        if not format:
            format = self.main_format
        url = self.build_url(track=track, artist=artist, method=method, format=format)
        return self.fetch(url)

    def fetch(self, url):
        try:
            df = pd.read_json(url)
            df["status"] = "success"
        except Exception as e:
            print(str(e))
            df = pd.DataFrame({
                "status": "error",
                "msg": str(e),
            })
        finally:
            return df
        # df = pd.DataFrame(df['result'].values.tolist())


# lastFM = LastFMInterface()
# url = lastFM.build_url(track="Love The Way You Lie", artist="Eminem", method="track.getInfo")
# print(url)
# lastFM.fetch(url)
