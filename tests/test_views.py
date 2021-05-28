def test_root(client):
    resp = client.get('/')
    assert b'Envio' in resp.data
