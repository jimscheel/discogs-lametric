from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

BASE_URL_TEMPLATE = "https://api.discogs.com/users/{username}/collection/folders/0/releases"

def get_collection(username, token):
    response = requests.get(
        BASE_URL_TEMPLATE.format(username=username),
        params={
            "token": token,
            "per_page": 100,
            "page": 1,
            "sort": "added",
            "sort_order": "desc"
        }
    )
    response.raise_for_status()
    data = response.json()
    return data.get("releases", [])

@app.route("/discogs/latest")
def latest():
    username = request.args.get("username")
    token = request.args.get("token")

    if not username or not token:
        return jsonify({
            "frames": [{
                "icon": "i5555",
                "text": "Missing username/token"
            }]
        }), 400

    try:
        releases = get_collection(username, token)
        latest = releases[0]["basic_information"]
        artist = latest["artists"][0]["name"]
        title = latest["title"]
        media_format = latest["formats"][0]["name"]
        return jsonify({
            "frames": [{
                "icon": 68832,
                "text": f"LATEST MEDIA TO COLLECTION: {artist} – {title} ({media_format})"
            }]
        })
    except Exception as e:
        return jsonify({
            "frames": [{
                "icon": "i5555",
                "text": f"Error: {str(e)}"
            }]
        }), 500

@app.route("/discogs/random")
def random_album():
    username = request.args.get("username")
    token = request.args.get("token")

    if not username or not token:
        return jsonify({
            "frames": [{
                "icon": "i5555",
                "text": "Missing username/token"
            }]
        }), 400

    try:
        releases = get_collection(username, token)
        album = random.choice(releases)["basic_information"]
        artist = album["artists"][0]["name"]
        title = album["title"]
        media_format = album["formats"][0]["name"]
        return jsonify({
            "frames": [{
                "icon": 68832,
                "text": f"TODAYS RANDOM ALBUM: {artist} – {title} ({media_format})"
            }]
        })
    except Exception as e:
        return jsonify({
            "frames": [{
                "icon": "i5555",
                "text": f"Error: {str(e)}"
            }]
        }), 500

@app.route("/discogs/count")
def count():
    username = request.args.get("username")
    token = request.args.get("token")

    if not username or not token:
        return jsonify({
            "frames": [{
                "icon": "i5555",
                "text": "Missing username/token"
            }]
        }), 400

    try:
        releases = get_collection(username, token)
        counts = {}

        for release in releases:
            basic = release.get("basic_information", {})
            formats = basic.get("formats", [])
            for fmt in formats:
                fmt_name = fmt.get("name", "").lower()
                desc = fmt.get("descriptions", [])
                all_names = [fmt_name] + [d.lower() for d in desc]

                for name in all_names:
                    if name in ["vinyl", "cd", "cassette"]:
                        counts[name] = counts.get(name, 0) + 1

        parts = [f"{k.upper()}={v}" for k, v in counts.items() if v > 0]
        count_text = " ".join(parts)

        return jsonify({
            "frames": [{
                "icon": 68832,
                "text": f"TOTAL MEDIA:  {count_text}"
            }]
        })
    except Exception as e:
        return jsonify({
            "frames": [{
                "icon": "i5555",
                "text": f"Error: {str(e)}"
            }]
        }), 500
