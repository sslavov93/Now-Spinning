class TestWebApp:
    def test_now_playing_endpoint_with_default_values(self, client):
        resp = client.get("/now-playing")
        assert b"N/A" in resp.data
