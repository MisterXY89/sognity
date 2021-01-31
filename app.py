
from flask import render_template, request, redirect, url_for, Response, send_from_directory, jsonify

import io
import csv
from flask import make_response

from app_init import app, resource_path, sp, sp_art


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
	if not "uri" in request.args:
		return False
	uri = request.args["uri"]
	item_id = uri.split(":")[-1]
	if "track" in uri:
		data_df = sp_art.gen_art_data(sp_art.test_playlist)
	elif "playlist" in uri:
		data_df = sp_art.gen_playlist_pic(sp_art.test_playlist)
		
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


if __name__ == '__main__':
	app.run()
