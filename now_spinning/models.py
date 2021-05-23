from now_spinning import db


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True, nullable=False)
    artist = db.Column(db.String(128), unique=True, nullable=False)
    year = db.Column(db.String(4), unique=True, nullable=False)
    # image_location = db.Column(db.String(512), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.artist} - {self.title} ({self.year})"
