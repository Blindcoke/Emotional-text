import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture
def test_predict(client):    
    response = client.post("/predict", json={"text": "Hello World! How are you?"})
    assert response.status_code == 200
    assert response.json() == {
        "predictions": ["neutral", "curiosity"],
        "sentences": ["Hello World", " How are you"],
        "symbol_emojies": ["! ", "? "]
    }

def test_transcribe(client):
    response = client.post("/transcribe", files={"audio": open("audio.mp3", "rb")})
    assert response.status_code == 200
    assert response.json() == {
        "predictions": ["neutral"],
        "sentences": ["Deep dark fantasies"],
        "symbol_emojies": [" "]
    }