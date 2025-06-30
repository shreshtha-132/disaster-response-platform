def test_add_resource(client, created_disaster):
    payload = {
        "disaster_id": str(created_disaster),
        "name": "Medical Camp",
        "location_name": "Connaught Place, Delhi",
        "type": "medical"
    }
    response = client.post("/resources", json=payload)
    assert response.status_code == 200
    assert "Resource Created" in response.json()["message"]

def test_get_resources_by_disaster(client, created_disaster):
    response = client.get(f"/resources/{created_disaster}/resources")
    assert response.status_code == 200
    assert "Resources" in response.json()
