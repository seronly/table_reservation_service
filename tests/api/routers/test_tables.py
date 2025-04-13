from fastapi.testclient import TestClient


def test_create_and_delete_table(client: TestClient) -> None:
    data = {"name": "Table 1", "seats": 4, "location": "зал у окна"}
    response = client.post("/api/tables", json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["seats"] == data["seats"]
    assert content["location"] == data["location"]

    table_id = content["id"]
    response = client.delete(f"/api/tables/{table_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Table succesfully deleted"
    response = client.delete(f"/api/tables/{table_id}")
    assert response.status_code != 200
    content = response.json()
    assert content["message"] == "Table can't be deleted"
