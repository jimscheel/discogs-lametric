from flask import Flask, jsonify, request
import requests
import random
import datetime
from collections import Counter

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
    random.seed(datetime.date.today().isoformat())
    album_info = random.choice(releases)["basic_information"]
    artist = album_info["artists"][0]["name"]
    title = album_info["title"]
    format_info = album_info.get("formats", [{}])[0]
    media_type = format_info.get("name", "Unknown")
    text = f"TODAYS RANDOM ALBUM: {artist} – {title} ({media_type})"
    return jsonify({"frames": [{"text": text, "icon": "68832"}]})

@app.route("/discogs/count")
def count():
    username = request.args.get("username")
    token = request.args.get("token")
    all_releases = []
    page = 1
    while True:
        url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"
        params = {
            "token": token,
            "per_page": 100,
            "page": page,
            "sort": "added",
            "sort_order": "desc"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        releases = data.get("releases", [])
        all_releases.extend(releases)
        if page >= data.get("pagination", {}).get("pages", 1):
            break
        page += 1

    counter = Counter()
    for release in all_releases:
        formats = release.get("basic_information", {}).get("formats", [])
        if formats:
            name = formats[0].get("name", "").lower()
            if name in ["vinyl", "cd", "cassette"]:
                counter[name] += 1

    parts = []
    if counter["vinyl"] > 0:
        parts.append(f"VINYL={counter['vinyl']}")
    if counter["cd"] > 0:
        parts.append(f"CD={counter['cd']}")
    if counter["cassette"] > 0:
        parts.append(f"CASSETTE={counter['cassette']}")

    text = "TOTAL MEDIA: " + " ".join(parts)
    return jsonify({"frames": [{"text": text, "icon": "68832"}]})
