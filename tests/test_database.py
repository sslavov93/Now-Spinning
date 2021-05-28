import json
import os
import tempfile

import pytest

from now_spinning import db
from now_spinning.database import import_track_data, export_track_data, add_new_track, delete_track_data_by_id


from now_spinning.models import Track


class TestTrackDataImport:
    def test_db_import_for_not_existing_file(self, setup):
        path = "/not/existing/file/path"

        with pytest.raises(FileNotFoundError):
            import_track_data(path)

    def test_db_import_for_empty_file(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write('')
            with pytest.raises(json.decoder.JSONDecodeError):
                import_track_data(path)

        finally:
            os.remove(path)

    def test_db_import_for_file_with_whitespaces(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(' ')
            with pytest.raises(json.decoder.JSONDecodeError):
                import_track_data(path)
        finally:
            os.remove(path)

    def test_db_import_for_file_with_partial_json_formatting(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write('{"')
            with pytest.raises(json.decoder.JSONDecodeError):
                import_track_data(path)
        finally:
            os.remove(path)

    def test_db_import_for_file_with_missing_tracks_field(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write('{"some_field": []}')
            with pytest.raises(ValueError):
                import_track_data(path)

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

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(contents)
            with pytest.raises(ValueError):
                import_track_data(path)
            res = Track.query.all()

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

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(contents)
            with pytest.raises(ValueError):
                import_track_data(path)
            res = Track.query.all()

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

            with pytest.raises(ValueError):
                import_track_data(path)

            res = Track.query.all()
            assert 1 == len(res)
        finally:
            os.remove(path)


class TestTrackDataExport:
    def test_data_export_when_no_data_in_table(self, setup):
        fd, path = tempfile.mkstemp()
        try:
            expected_msg = f"Track data exported in {path}."
            expected_contents = """{"tracks": []}"""

            actual_msg = export_track_data(path)
            with os.fdopen(fd, 'r') as tmp:
                actual_contents = tmp.read()

            assert expected_contents == actual_contents
            assert expected_msg == actual_msg

        finally:
            os.remove(path)

    def test_data_export_when_single_track_in_table(self, setup):
        db.session.add(Track(artist="artist", title="title", year=123))
        db.session.commit()

        fd, path = tempfile.mkstemp()
        try:
            expected_msg = f"Track data exported in {path}."
            expected_contents = """{"tracks": [{"artist": "artist", "title": "title", "year": 123}]}"""

            actual_msg = export_track_data(path)
            with os.fdopen(fd, 'r') as tmp:
                actual_contents = tmp.read()

            assert expected_contents == actual_contents
            assert expected_msg == actual_msg

        finally:
            os.remove(path)

    def test_data_export_when_multiple_tracks_in_table(self, setup):
        db.session.add_all([
            Track(artist="artist", title="title", year=123),
            Track(artist="artist2", title="title2", year=123)
        ])
        db.session.commit()

        fd, path = tempfile.mkstemp()
        try:
            expected_msg = f"Track data exported in {path}."
            expected_contents = """{"tracks": [{"artist": "artist", "title": "title", "year": 123}, {"artist": "artist2", "title": "title2", "year": 123}]}"""

            actual_msg = export_track_data(path)
            with os.fdopen(fd, 'r') as tmp:
                actual_contents = tmp.read()

            assert expected_contents == actual_contents
            assert expected_msg == actual_msg

        finally:
            os.remove(path)


class TestAddNewTrack:
    def test_add_new_track_when_some_metadata_is_missing_expect_error(self, setup):
        with pytest.raises(ValueError):
            add_new_track("", "Envio", 2004)

    def test_add_a_track(self, setup):
        expected_msg = "Added 'For You'."

        actual_msg = add_new_track("For You", "Envio", 2005)
        all_tracks = Track.query.all()
        res = Track.query.filter(Track.title == "For You").all()

        assert expected_msg == actual_msg
        assert 1 == len(all_tracks)
        assert 1 == len(res)


class TestDeleteTrack:
    def test_delete_a_track_by_id_if_track_is_not_present(self, setup, add_track):
        delete_track_data_by_id(3)

        db_size = Track.query.all()
        assert 1 == len(db_size)

    def test_delete_a_track_by_id_if_track_is_present(self):
        delete_track_data_by_id(1)

        db_size = Track.query.all()
        assert 0 == len(db_size)
