from flask import Flask, jsonify, request
import requests
import random

app = Flask(__name__)

def get_collection(username, token):
    url = f"https://api.discogs.com/users/{username}/collection/folders/0/releases"
    response = requests.get(url, params={"token": token, "per_page": 100, "page": 1})
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
    return jsonify({"frames": [{"text": f"{artist} – {title}", "icon": "i1234"}]})

@app.route("/discogs/random")
def random_album():
    username = request.args.get("username")
    token = request.args.get("token")
    releases = get_collection(username, token)
    album = random.choice(releases)["basic_information"]
    artist = album["artists"][0]["name"]
    title = album["title"]
    return jsonify({"frames": [{"text": f"{artist} – {title}", "icon": "i2222"}]})

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
