import json
import os

from now_spinning import db
from now_spinning.models import Track


# TODO - Add track data validation
# TODO This requires some exception handling
def import_track_data(path: str):
    if not os.path.exists(path):
        return f"Cannot import data from '{path}' - File Not Found - abort."

    try:
        with open(path, "r") as f:
            data = json.loads(f.read())
            if "tracks" not in data:
                return "Missing required 'tracks' field - abort."

            tracks = []
            for track in data.get("tracks"):
                if not track.get("title") or not track.get("artist"):
                    return "Missing track data - abort."
                tracks.append(Track(
                    title=track.get("title"),
                    artist=track.get("artist"),
                    year=track.get("year"),
                ))
            db.drop_all()
            db.create_all()
            db.session.add_all(tracks)
            db.session.commit()
        return "Successful import."

    except json.decoder.JSONDecodeError:
        return "Incorrect file formatting - abort."


# TODO This requires some exception handling
def export_track_data(path: str):
    all_tracks_result = Track.query.all()
    export_data = {"tracks": []}
    for track in all_tracks_result:
        export_data["tracks"].append({"artist": track.artist, "title": track.title, "year": track.year})
    with open(path, "w") as f:
        f.write(json.dumps(export_data))

    return f"Track data exported in {path}."


# TODO This requires some exception handling
def add_new_track(title: str, artist: str, year: int):
    if not title or not artist or not year:
        return "Failed to add new track - missing metadata."

    db.session.add(Track(title=title, artist=artist, year=year))
    db.session.commit()
    return f"Added '{title}'."
