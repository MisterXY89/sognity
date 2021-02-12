
from flask import render_template, request, redirect, url_for, Response, send_from_directory, jsonify

import io
import csv
from flask import make_response

from app_init import app, resource_path, sp, sp_art, sw_lyrics, sentiment, lastFM
from src.helper import ms_to_mins


@app.route('/')
def index():
	return render_template("index.html")

@app.route("/test")
def test():
	data = sp_art.gen_art_data(sp_art.test_id)
	return render_template("test.html", data=data)


@app.route('/data/<path:path>')
def send_js(path):
    """
    enable reading from data folder
    """
    return send_from_directory('data', path)


@app.route("/read-art-data")
def read_art_data():
	if not "uri" in request.args and not "sentiment" in request.args:
		return False
	uri = request.args["uri"]
	sentiment = request.args["sentiment"]
	item_id = uri.split(":")[-1]
	if "track" in uri:
		data_df = sp_art.gen_art_data(item_id, sentiment=sentiment, return_df=True, pl=False)
	elif "playlist" in uri:
		data_df = sp_art.gen_playlist_pic(item_id)

	resp = make_response(data_df.to_csv())
	resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
	resp.headers["Content-Type"] = "text/csv"
	return resp

@app.route("/start")
def start():
    return render_template("index.html")


@app.route("/search")
def search():
	data = request.args
	if "q" in data:
		query = str(data["q"])
		if query:
			return jsonify(sp.search(query))
	return "Error: no query provied or emtpy"


# const URI = "spotify:playlist:0VOTzMhgX9JA2YHXRl1Vqr";
# "spotify:playlist:2QdD7JXzIpyapcfF2QZbUB"
@app.route("/result")
def result():
	req_data = request.args
	if not "uri" in req_data:
		return False
	uri = req_data["uri"]
	item_id = uri.split(":")[-1]
	media_data = sp.get_info(item_id)
	# print(media_data)
	title = media_data["name"]
	artists = list(map(lambda a: a["name"], media_data["artists"]))
	lyrics = sw_lyrics.get_lyrics(title, artists[0]).replace("\n", "<br>")
	analysis_data = sp.features(item_id)[0]
	sentiment_scores = sentiment.get_scores(lyrics)
	song_info = lastFM.get(track=title, artist=artists[0], method="track.getInfo")["track"]
	summary = song_info["wiki"]["summary"].replace("\n", "<br>").replace("Read more on Last.fm", "").replace("</a>.", "</a>")
	similar_tracks = lastFM.get(track=title, artist=artists[0])
	data = {
		"media" : {
			"uri": uri,
			"title": title,
			"artist": ",".join(artists),
			"album": {
				"name": media_data["album"]["name"],
				"image_url_md": media_data["album"]["images"][1]["url"],
				"image_url_lg": media_data["album"]["images"][0]["url"],
			},
			"lyrics": lyrics,
			"length": ms_to_mins(media_data["duration_ms"]),
			"href": analysis_data["track_href"],
			"preview_url": media_data["preview_url"],
			"summary": summary,
			"similar_tracks": similar_tracks,
		},
		"treemap": {
			"selector": "#song-treemap",
			"height": 200,
			"width": 200,
		},
		"analysis": {
			"valence": analysis_data["valence"],
			"energy": analysis_data["energy"],
			"danceability": analysis_data["danceability"],
			"sentiment_string": sentiment.get_sentiment_string(sentiment_scores),
			"sentiment_scores": sentiment_scores,
		},
	}
	# print(data)
	return render_template("fact_sheet.html", data=data)


if __name__ == '__main__':
	app.run()
