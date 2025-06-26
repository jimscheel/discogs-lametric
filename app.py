
from flask import Flask, jsonify, request
import requests
import random

app = Flask(__name__)

def get_collection(username, token):
    if not username or not token:
        return None, "Missing username or token"
    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"
    response = requests.get(url, params={"token": token, "per_page": 100, "page": 1, "sort": "added", "sort_order": "desc"})
    if response.status_code != 200:
        return None, "Failed to fetch data from Discogs"
    return response.json().get("releases", []), None

@app.route("/discogs/latest")
def latest():
    username = request.args.get("username")
    token = request.args.get("token")
    releases, error = get_collection(username, token)
    if error:
        return jsonify({"frames": [{"icon": "i5555", "text": error}]}), 400
    latest = releases[0]["basic_information"]
    artist = latest["artists"][0]["name"]
    title = latest["title"]
    media = releases[0].get("format", [{}])[0].get("name", "Media")
    return jsonify({"frames": [{"text": f"LATEST MEDIA TO COLLECTION: {artist} – {title} ({media})", "icon": "68832"}]})

@app.route("/discogs/random")
def random_album():
    username = request.args.get("username")
    token = request.args.get("token")
    releases, error = get_collection(username, token)
    if error:
        return jsonify({"frames": [{"icon": "i5555", "text": error}]}), 400
    album = random.choice(releases)["basic_information"]
    artist = album["artists"][0]["name"]
    title = album["title"]
    media = releases[random.randint(0, len(releases)-1)].get("format", [{}])[0].get("name", "Media")
    return jsonify({"frames": [{"text": f"TODAYS RANDOM ALBUM: {artist} – {title} ({media})", "icon": "68832"}]})

@app.route("/discogs/count")
def count():
    username = request.args.get("username")
    token = request.args.get("token")
    releases, error = get_collection(username, token)
    if error:
        return jsonify({"frames": [{"icon": "i5555", "text": error}]}), 400
    counts = {}
    for release in releases:
        format_name = release.get("format", [{}])[0].get("name", "Unknown").lower()
        if format_name in ["vinyl", "cd", "cassette"]:
            counts[format_name] = counts.get(format_name, 0) + 1
    parts = [f"{k.upper()}={v}" for k, v in counts.items() if v > 0]
    return jsonify({"frames": [{"text": f"TOTAL MEDIA:  {' '.join(parts)}", "icon": "68832"}]})
