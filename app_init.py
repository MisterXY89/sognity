
import os
import time
import json
from flask import Flask

from src.spotify import sp_interface, spoti_art
from src.song_data import lyrics as sw_lyrics
from src.song_data import last_fm_interface
from src.analysis import sentiment

app = Flask("Sognity", static_url_path='')
app.config['FLASK_SECRET'] = 'VA/EVGoSYda;#EL'

# set timezone:
os.environ['TZ'] = 'Europe/Berlin'
time.tzset()

resource_path = os.path.join(app.root_path, 'data')


############################################################

sp = sp_interface.SpotifyInterface()
sp_art = spoti_art.SpotiArt(size=500)
sentiment = sentiment.SentimentAnalyzer()
lastFM = last_fm_interface.LastFMInterface()

# get_lyrics = sw_lyrics.get_lyrics
