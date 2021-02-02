
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
        self.colors = {
            # "negative": ["#890641", "#F72585", "#7E106E", "#7209B7", "#560BAD", "#480CA8", "#3A0CA3", "#3F37C9", "#4361EE", "#4CC9F0", "#B4E9F9"],
            "negative": ["#27003D", "#7400B8", "#6930C3", "#5E60CE", "#5390D9", "#4EA8DE", "#48BFE3", "#56CFE1", "#64DFDF", "#72EFDD", "#80FFDB"],
            "neutral" : ["#F8F9FA", "#E9ECEF", "#DEE2E6", "#CED4DA", "#ADB5BD", "#6C757D", "#495057", "#343A40", "#212529", "#121417", "#090A0B"],
            "positive": ["#003D2E", "#007F5F", "#2B9348", "#55A630", "#80B918", "#AACC00", "#BFD200", "#D4D700", "#DDDF00", "#EEEF20", "#FFFF3F"]
        }

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

    def gen_art_data(self, track_id, valence=None, sentiment="", return_df=False, pl=True):
        """
        duration sets size loudness sets tone, key sets color/ mode darkness
        tempo amount of noise points (random black ones)
        """
        art_list = []
        parent = "root" if pl else ""
        treemap_list = [{
            "name": track_id,
            "parent": parent,
            "value": "",
            "color": "",
            "loudness": "",
            "key": "",
            "tempo": "",
        }]
        sections_df = self.get_section_df(track_id)
        selected_color_pal = self.colors[sentiment]
        for i, row in sections_df.iterrows():
            color_index = int(row["key"]) % (len(selected_color_pal))
            section_size = math.sqrt(row["duration"] * (self.size * self.size))
            main_color = selected_color_pal[color_index]
            tempo = row["tempo"]
            hsv_color = Color(hex=main_color).hsv
            new_saturation = hsv_color[1] * (1-abs(row["loudness"]*(tempo/100)))
            new_hex = Color(hsv=(hsv_color[0], new_saturation, hsv_color[2])).hex

            treemap_list.append({
                # "name": f"{track_id[:2]}_{i}",
                "name": i,
                "parent": track_id,
                "value": section_size,
                "color": new_hex,
                "loudness": row["loudness"],
                "key": row["key"],
                "tempo": row["tempo"],
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
