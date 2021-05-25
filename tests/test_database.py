import os
import tempfile

import pytest

from now_spinning import db
from now_spinning.database import import_track_data


from now_spinning.models import Track


class TestTrackDataImport:
    @pytest.fixture
    def setup(self):
        db.drop_all()
        db.create_all()

    @pytest.fixture
    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_db_import_for_not_existing_file(self, setup):
        path = "/not/existing/file/path"
        expected = f"Cannot import data from '{path}' - File Not Found - abort."

        actual = import_track_data(path)

        assert expected == actual

    def test_db_import_for_empty_file(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write('')
            expected = "Incorrect file formatting - abort."
            actual = import_track_data(path)

            assert expected == actual
        finally:
            os.remove(path)

    def test_db_import_for_file_with_whitespaces(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(' ')
            expected = "Incorrect file formatting - abort."
            actual = import_track_data(path)

            assert expected == actual
        finally:
            os.remove(path)

    def test_db_import_for_file_with_partial_json_formatting(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write('{"')
            expected = "Incorrect file formatting - abort."
            actual = import_track_data(path)

            assert expected == actual
        finally:
            os.remove(path)

    def test_db_import_for_file_with_missing_tracks_field(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write('{"some_field": []}')
            expected = "Missing required 'tracks' field - abort."
            actual = import_track_data(path)

            assert expected == actual
        finally:
            os.remove(path)

    def test_db_import_for_file_with_no_tracks_expect_empty_database(self, setup):
        contents = '''
    {"tracks": []}'''
        expected_msg = "Successful import."

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(contents)
            actual_msg = import_track_data(path)
            res = Track.query.all()

            assert 0 == len(res)
            assert expected_msg == actual_msg

        finally:
            os.remove(path)

    def test_db_import_for_file_with_one_tracks_expect_one_row_in_db(self, setup):
        contents = '''
    {"tracks": [
        {
            "artist": "Envio",
            "title": "Time To Say Goodbye (Original Mix)",
            "year": 2004
        }
    ]}'''
        expected_msg = "Successful import."

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(contents)
            actual_msg = import_track_data(path)
            res = Track.query.all()

            assert 1 == len(res)
            assert expected_msg == actual_msg

        finally:
            os.remove(path)

    def test_db_import_for_file_with_multiple_tracks_expect_one_row_in_db(self, setup):
        contents = '''
    {"tracks": [
        {
            "artist": "Envio",
            "title": "Time To Say Goodbye (Original Mix)",
            "year": 2004
        },
        {
            "artist": "Envio",
            "title": "For You (Original Mix)",
            "year": 2006
        }
    ]}'''
        expected_msg = "Successful import."

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(contents)
            actual_msg = import_track_data(path)
            res = Track.query.all()

            assert 2 == len(res)
            assert expected_msg == actual_msg

        finally:
            os.remove(path)

    def test_import_when_track_title_is_empty_expect_no_op(self, setup):
        contents = '''
        {"tracks": [
            {
                "artist": "Envio",
                "title": "",
                "year": 2004
            }
        ]}'''
        expected_msg = "Missing track data - abort."

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(contents)
            actual_msg = import_track_data(path)
            res = Track.query.all()

            assert expected_msg == actual_msg
            assert 0 == len(res)

        finally:
            os.remove(path)

    def test_import_when_track_artist_is_empty_expect_no_op(self, setup):
        contents = '''
        {"tracks": [
            {
                "artist": "",
                "title": "Time To Say Goodbye (Original Mix)",
                "year": 2004
            }
        ]}'''
        expected_msg = "Missing track data - abort."

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(contents)
            actual_msg = import_track_data(path)
            res = Track.query.all()

            assert expected_msg == actual_msg
            assert 0 == len(res)

        finally:
            os.remove(path)

    def test_import_when_data_in_db_and_new_data_corrupt_expect_no_op(self, setup):
        db.session.add(Track(artist="artist", title="title", year=123))
        db.session.commit()

        res = Track.query.all()
        assert 1 == len(res)

        contents = '''
            {"tracks": [
                {
                    "artist": "",
                    "title": "Time To Say Goodbye (Original Mix)",
                    "year": 2004
                },
                {
                    "artist": "Envio",
                    "title": "For You (Original Mix)",
                    "year": 2006
                }
            ]}'''

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(contents)

            expected_msg = "Missing track data - abort."
            actual_msg = import_track_data(path)
            assert expected_msg == actual_msg

            res = Track.query.all()
            assert 1 == len(res)
        finally:
            os.remove(path)



