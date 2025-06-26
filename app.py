from flask import Flask, request, jsonify
import requests

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
