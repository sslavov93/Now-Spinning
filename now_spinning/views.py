import json

from flask import current_app as app, request, render_template, jsonify, send_from_directory
from now_spinning import db
from now_spinning.models import Track

cache = {"title": "N/A", "artist": "N/A"}


@app.route("/now-playing")
def now_playing():
    return render_template(
        "now_playing.html",
        title=cache.get("title"),
        artist=cache.get("artist"),
        year=cache.get("year"),
        image_location=cache.get("image_location"),
    )


@app.route("/api/v1/switch", methods=["POST"])
def switch_now_playing_track():
    data = request.get_json()
    t = Track.query.get(data.get("track_id"))
    cache.update({"artist": t.artist, "year": t.year, "title": t.title, "image_location": t.image_location})
    return "track switched"


@app.route("/api/v1/static/<path:path>")
def static_dir(path):
    return send_from_directory(app.config.get("MEDIA_FOLDER"), path)


@app.route("/api/v1/tracks", methods=["POST"])
def add_new_track():
    data = request.get_json()
    t = Track(
        title=data.get("title"),
        artist=data.get("artist"),
        year=data.get("year"),
        image_location=data.get("image_location")
    )

    db.session.add(t)
    db.session.flush()
    db.session.commit()

    return jsonify({"title": data.get("title"), "artist": data.get("artist")})


@app.route("/")
def hello():
    # db.drop_all()
    tracks = Track.query.all()
    if len(tracks) < 1:
        return render_template("index.html")
    else:
        return render_template("tracks_home.html", tracks=tracks)
    # with open(app.config.get("TRACK_METADATA"), "r") as f:
    #     data = json.loads(f.read())
    #     if "tracks" not in data:
    #         raise ValueError("Missing required 'tracks' field - abort.")
    #
    #     tracks = []
    #     for track in data.get("tracks"):
    #         if not track.get("title") or not track.get("artist"):
    #             raise ValueError("Missing track data - abort.")
    #         tracks.append(
    #             Track(
    #                 title=track.get("title"),
    #                 artist=track.get("artist"),
    #                 year=track.get("year"),
    #                 image_location=track.get("image_location"),
    #             )
    #         )
    #     db.drop_all()
    #     db.create_all()
    #     db.session.add_all(tracks)
    #     db.session.commit()

    return "data imported"
