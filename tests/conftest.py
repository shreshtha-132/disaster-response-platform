#test setup file
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def created_disaster(client):
    payload = {
        "title": "Test Earthquake",
        "description": "A large earthquake in Delhi",
        "tags":["earthquake"],
        "owner_id": "netrunnerX"
    }
    response = client.post("/disasters", json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    return data[0]["id"]