import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.main import app
from app.models.table import Table
from app.schemas.table import Table, TableCreate
from app.services import table_services
from fastapi import status

client = TestClient(app)

# Тестовые данные
table = Table(
    id=1,
    name="Table 1",
    seats=4,
    location="Main Hall"
)

table_create_json = {
    "name": "Table 1",
    "seats": 4,
    "location": "Main Hall"
}

# Тесты для GET /tables
@pytest.mark.asyncio
async def test_get_tables_success(monkeypatch, client):
    mock_get_tables = AsyncMock(return_value=[table])
    monkeypatch.setattr(table_services, "get_tables", mock_get_tables)

    response = client.get("/api/tables/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [table_create_json | {"id": 1}]
    mock_get_tables.assert_called_once()

@pytest.mark.asyncio
async def test_get_tables_not_found(monkeypatch, client):
    mock_get_tables = AsyncMock(return_value=[])
    monkeypatch.setattr(table_services, "get_tables", mock_get_tables)

    response = client.get("/api/tables/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Tables not found"}
    mock_get_tables.assert_called_once()

@pytest.mark.asyncio
async def test_create_table_success(monkeypatch, mock_session, client):
    mock_create_table = AsyncMock(return_value=table)
    monkeypatch.setattr(table_services, "create_table", mock_create_table)

    response = client.post("/api/tables/", json=table_create_json)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == table_create_json | {"id": 1}
    mock_create_table.assert_called_once()

@pytest.mark.asyncio
async def test_create_table_failed(monkeypatch, mock_session, client):
    mock_create_table = AsyncMock(return_value=None)
    monkeypatch.setattr(table_services, "create_table", mock_create_table)

    response = client.post("/api/tables/", json=table_create_json)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Table not created"}
    mock_create_table.assert_called_once()

@pytest.mark.asyncio
async def test_create_table_invalid_data(client):
    invalid_data = table_create_json.copy()
    invalid_data["seats"] = 0

    response = client.post("/api/tables/", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_create_table_empty_name(client):
    invalid_data = table_create_json.copy()
    invalid_data["name"] = ""

    response = client.post("/api/tables/", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_create_table_too_long_name(client):
    invalid_data = table_create_json.copy()
    invalid_data["name"] = "A" * 101

    response = client.post("/api/tables/", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_delete_table_success(monkeypatch, client):
    mock_delete_table = AsyncMock(return_value=True)
    monkeypatch.setattr(table_services, "delete_table_by_id", mock_delete_table)

    response = client.delete("/api/tables/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Table with id 1 deleted"}
    mock_delete_table.assert_called_once()

@pytest.mark.asyncio
async def test_delete_table_not_found(monkeypatch, client):
    mock_delete_table = AsyncMock(return_value=False)
    monkeypatch.setattr(table_services, "delete_table_by_id", mock_delete_table)

    response = client.delete("/api/tables/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Table with id 999 not found"}
    mock_delete_table.assert_called_once()

@pytest.mark.asyncio
async def test_delete_table_invalid_id(client):
    response = client.delete("/api/tables/-1")
    print(response.json())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()
