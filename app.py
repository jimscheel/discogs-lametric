from flask import Flask, jsonify, request
import requests
import random
import os

app = Flask(__name__)

USERNAME = os.getenv("DISCOGS_USERNAME")
TOKEN = os.getenv("DISCOGS_TOKEN")
BASE_URL = f"https://api.discogs.com/users/{USERNAME}/collection/folders/0/releases"

def get_collection():
    response = requests.get(BASE_URL, params={"token": TOKEN, "per_page": 100, "page": 1})
    response.raise_for_status()
    data = response.json()
    return data.get("releases", [])

@app.route("/discogs/latest")
def latest():
    releases = get_collection()
    latest = releases[0]["basic_information"]
    artist = latest["artists"][0]["name"]
    title = latest["title"]
    return jsonify({"frames": [{"text": f"{artist} – {title}", "icon": "i1234"}]})

@app.route("/discogs/random")
def random_album():
    releases = get_collection()
    album = random.choice(releases)["basic_information"]
    artist = album["artists"][0]["name"]
    title = album["title"]
    return jsonify({"frames": [{"text": f"{artist} – {title}", "icon": "i2222"}]})

@app.route("/discogs/count")
def count():
    response = requests.get(BASE_URL, params={"token": TOKEN})
    response.raise_for_status()
    data = response.json()
    total = data.get("pagination", {}).get("items", 0)
    return jsonify({"frames": [{"text": f"Du har {total} plader", "icon": "i3333"}]})
