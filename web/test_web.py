import pytest
from web import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)

def test_read(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_submit(client):
    response = client.post("/submit", json={"text": "Hello World! How are you?"})
    assert response.status_code == 200
    predictions = []
    print(predictions)
    for sublist in response.json()['predictions']:
            predictions.append(sublist[0]['label'])
    
    assert predictions == ["neutral", "curiosity"]
    assert response.json()["sentences"] == ["Hello World", "How are you"]
    assert response.json()["symbol_emojies"] == ["! ", "? "]  

def test_submit_audio(client):
    response = client.post("/submit_voice", files={"audioFile": open("./ai/audio3.mp3", "rb")})
    assert response.status_code == 200
    predictions = []
    for sublist in response.json()['predictions']:
            predictions.append(sublist[0]['label'])
    assert predictions == ["neutral"]
    assert response.json()["sentences"] == [" dungeon in my house"]
    assert response.json()["symbol_emojies"] == ['. ']