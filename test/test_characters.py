from fastapi.testclient import TestClient

from  src.api.server import app

import json

client = TestClient(app)

def test_get_character():
    response = client.get("/characters/7421")
    assert response.status_code == 200

    with open('test/characters/7421.json') as f:
        assert response.json() == json.load(f)

def test_characters():
    response = client.get("/characters/")
    assert response.status_code == 200

    with open('test/characters/root.json') as f:
        assert response.json() == json.load(f)