import uuid
DISASTER_ID = None

def test_get_disasters(client):
    response = client.get("/disasters")
    assert response.status_code==200
    assert "disasters" in response.json()

def test_create_disasters(created_disaster):
    assert created_disaster is not None

    
    
def test_get_disaster_by_id(client,created_disaster):
    response = client.get(f"/disasters/{created_disaster}")
    assert response.status_code == 200
    assert response.json()["disaster"]["id"] == created_disaster