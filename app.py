
from flask import render_template, request, redirect, url_for, Response, send_from_directory, jsonify

from app_init import app, resource_path, sp


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/data/<path:path>')
def send_js(path):
    """
    enable reading from data folder
    """
    return send_from_directory('data', path)


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
