from now_spinning import db


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), unique=False, nullable=False)
    artist = db.Column(db.String(10), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=True)
    image_location = db.Column(db.String(512), unique=False, nullable=True)

    def __repr__(self):
        return f"<Track(id={self.id},title={self.title},artist={self.artist},year={self.artist})>"
