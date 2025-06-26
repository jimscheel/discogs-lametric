from flask import Flask, jsonify, request
import requests
import random

app = Flask(__name__)

def get_collection(username, token):
    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"
    params = {
        "token": token,
        "per_page": 100,
        "page": 1,
        "sort": "added",
        "sort_order": "desc"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("releases", [])

@app.route("/discogs/latest")
def latest():
    username = request.args.get("username")
    token = request.args.get("token")
    releases = get_collection(username, token)
    latest = releases[0]["basic_information"]
    artist = latest["artists"][0]["name"]
    title = latest["title"]
    format_info = latest.get("formats", [{}])[0]
    media_type = format_info.get("name", "Unknown")
    text = f"LATEST MEDIA TO COLLECTION: {artist} – {title} ({media_type})"
    return jsonify({"frames": [{"text": text, "icon": "68832"}]})

@app.route("/discogs/random")
def random_album():
    username = request.args.get("username")
    token = request.args.get("token")
    releases = get_collection(username, token)
    album_info = random.choice(releases)["basic_information"]
    artist = album_info["artists"][0]["name"]
    title = album_info["title"]
    format_info = album_info.get("formats", [{}])[0]
    media_type = format_info.get("name", "Unknown")
    text = f"RANDOM ALBUM FROM COLLECTION: {artist} – {title} ({media_type})"
    return jsonify({"frames": [{"text": text, "icon": "68832"}]})

@app.route("/discogs/count")
def count():
    username = request.args.get("username")
    token = request.args.get("token")
    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"
    response = requests.get(url, params={"token": token})
    response.raise_for_status()
    data = response.json()
    total = data.get("pagination", {}).get("items", 0)
    return jsonify({"frames": [{"text": f"Du har {total} plader", "icon": "i3333"}]})
