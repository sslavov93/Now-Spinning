from flask import current_app as app, render_template


cache = {"title": "N/A", "artist": "N/A"}


@app.route("/now-playing")
def now_playing():
    return render_template(
        "now_playing.html",
        title=cache.get("title"),
        artist=cache.get("artist"),
        year=cache.get("year"),
        image=cache.get("image"),
    )
