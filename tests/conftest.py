import pytest as pytest


from now_spinning import db, app
from now_spinning.database import init_db
from now_spinning.models import Track


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


@pytest.fixture
def setup():
    db.drop_all()
    db.create_all()


@pytest.fixture
def add_track():
    db.session.add(Track(title="title1", artist="artist1", year=2000))
