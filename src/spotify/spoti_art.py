
import math
import pandas as pd
from colorutils import Color

from .sp_interface import SpotifyInterface

class SpotiArt:
    """docstring for SpotiArt."""

    def __init__(self, size):
        self.size = size
        self.si = SpotifyInterface()
        self.test_id = "1CmRSaMG6t09K9avv7UhvB"
        self.test_playlist = "5ULAnTPk479ty7PGEY84AL"
        self.colors = ["#890641", "#F72585", "#7E106E", "#7209B7", "#560BAD", "#480CA8", "#3A0CA3", "#3F37C9", "#4361EE", "#4CC9F0", "#B4E9F9"]

    def get_section_df(self, track_id):
        """
        get and return a df for the sections whils standardizing duration to
        percentage of song and min/max norm loudness
        """
        analysis_res = self.si.analysis(track_id)
        # bars, beats, sections, segments, tatums
        sections_df = pd.DataFrame(analysis_res["sections"])
        sections_df = sections_df[["start", "duration", "loudness", "tempo", "key", "mode"]]
        sections_df["duration"] = sections_df["duration"] / sum(sections_df["duration"])
        sections_df["loudness"] = sections_df["loudness"].apply(lambda x: abs(x))
        sections_df["loudness"] = sections_df["loudness"] / sum(sections_df["loudness"])
        return sections_df

    def gen_art_data(self, track_id, return_df=False):
        """
        duration sets size loudness sets tone, key sets color/ mode darkness
        tempo amount of noise points (random black ones)
        """
        art_list = []
        treemap_list = [{
            # "name": "root",
            "name": track_id,
            "parent": "root",
            "value": ""
        }]
        sections_df = self.get_section_df(track_id)
        for i, row in sections_df.iterrows():
            color_index = int(row["key"]) % (len(self.colors))
            section_size = math.sqrt(row["duration"] * (self.size * self.size))
            main_color = self.colors[color_index]
            hsv_color = Color(hex=main_color).hsv
            new_saturation = hsv_color[1] * (1-abs(row["loudness"]))
            new_hex = Color(hsv=(hsv_color[0], new_saturation, hsv_color[2])).hex
            # art_list.append({
            #     "size": section_size,
            #     "main_color": main_color,
            #     "highlight_color": new_hex
            # })
            treemap_list.append({
                "name": f"{track_id[:2]}_{i}",
                "parent": track_id,
                "value": section_size,
                "color": new_hex,
            })

        if return_df:
            return pd.DataFrame(treemap_list)
        return treemap_list

    def gen_playlist_pic(self, playlist_id):
        playlist_tracks = self.si.get_tracks_from_playlist(playlist_id)
        playlist_pic_data_list = [{
            "name": "root",
            "parent": "",
            "value": ""
        }]
        for track_id in playlist_tracks:
            playlist_pic_data_list.extend(self.gen_art_data(track_id))

        return pd.DataFrame(playlist_pic_data_list)
