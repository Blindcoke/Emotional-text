import pytest
from web import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture
def test_read(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_submit(client):
    response = client.post("/submit", json={"text": "Hello World! How are you?"})
    assert response.status_code == 200
    assert response.json() == {
        "predictions": ["neutral", "curiosity"],
        "sentences": ["Hello World", " How are you"],
        "symbol_emojies": ["! ", "? "]
    }