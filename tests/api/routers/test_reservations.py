import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from app.main import app
from app.schemas.reservation import Reservation, ReservationCreate
from app.services import reservation_services, table_services
from fastapi import status

client = TestClient(app)

reservation = Reservation(
    customer_name="John Doe",
    reservation_time=datetime(2025, 4, 12, 12, 0, 0),
    duration_minutes=60,
    table_id=1,
    id=1,
)

reservation_create = ReservationCreate(
    customer_name="John Doe",
    reservation_time=datetime(2025, 4, 12, 12, 0, 0),
    duration_minutes=60,
    table_id=1,
)


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.mark.asyncio
async def test_get_reservations_success(monkeypatch, mock_session, client):
    mock_get_reservations = AsyncMock(return_value=[reservation])
    monkeypatch.setattr(reservation_services, "get_reservations", mock_get_reservations)

    response = client.get("/reservations/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [reservation.model_dump(mode="json", by_alias=True)]
    mock_get_reservations.assert_called_once_with(mock_session)


@pytest.mark.asyncio
async def test_get_reservations_not_found(monkeypatch, mock_session, client):
    mock_get_reservations = AsyncMock(return_value=[])
    monkeypatch.setattr(reservation_services, "get_reservations", mock_get_reservations)

    response = client.get("/reservations/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Reservations not found"}
    mock_get_reservations.assert_called_once_with(mock_session)


@pytest.mark.asyncio
async def test_create_reservation_success(monkeypatch, mock_session, client):
    mock_get_table = AsyncMock(return_value=MagicMock(id=1))
    mock_check_conflict = AsyncMock(return_value=False)
    mock_create_reservation = AsyncMock(return_value=reservation)

    monkeypatch.setattr(table_services, "get_table_by_id", mock_get_table)
    monkeypatch.setattr(
        reservation_services, "check_reservation_conflict", mock_check_conflict
    )
    monkeypatch.setattr(
        reservation_services, "create_reservation", mock_create_reservation
    )

    response = client.post("/reservations/", json=reservation_create.model_dump_json())

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "customer_name": "John Doe",
        "reservation_time": "2025-04-12T12:00:00",
        "duration_minutes": 60,
        "table_id": 1,
    }
    mock_get_table.assert_called_once_with(1, mock_session)
    mock_check_conflict.assert_called_once_with(
        datetime.fromisoformat("2025-04-12T12:00:00"), 60, 1, mock_session
    )
    mock_create_reservation.assert_called_once()


@pytest.mark.asyncio
async def test_create_reservation_table_not_found(monkeypatch, mock_session, client):
    mock_get_table = AsyncMock(return_value=None)
    monkeypatch.setattr(table_services, "get_table_by_id", mock_get_table)

    response = client.post("/reservations/", json=reservation_create.model_dump_json())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Table with id 1 not found"}
    mock_get_table.assert_called_once_with(1, mock_session)


@pytest.mark.asyncio
async def test_create_reservation_time_conflict(monkeypatch, mock_session, client):
    mock_get_table = AsyncMock(return_value=MagicMock(id=1))
    mock_check_conflict = AsyncMock(return_value=True)
    monkeypatch.setattr(table_services, "get_table_by_id", mock_get_table)
    monkeypatch.setattr(
        reservation_services, "check_reservation_conflict", mock_check_conflict
    )

    response = client.post("/reservations/", json=reservation_create.model_dump_json())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Time conflicts. This table is already reserved at this time"
    }
    mock_get_table.assert_called_once_with(1, mock_session)
    mock_check_conflict.assert_called_once_with(
        datetime.fromisoformat("2025-04-12T12:00:00"), 60, 1, mock_session
    )


@pytest.mark.asyncio
async def test_create_reservation_failed(monkeypatch, mock_session, client):
    mock_get_table = AsyncMock(return_value=MagicMock(id=1))
    mock_check_conflict = AsyncMock(return_value=False)
    mock_create_reservation = AsyncMock(return_value=None)

    monkeypatch.setattr(table_services, "get_table_by_id", mock_get_table)
    monkeypatch.setattr(
        reservation_services, "check_reservation_conflict", mock_check_conflict
    )
    monkeypatch.setattr(
        reservation_services, "create_reservation", mock_create_reservation
    )

    response = client.post("/reservations/", json=reservation_create.model_dump_json())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Reservation not created"}
    mock_get_table.assert_called_once_with(1, mock_session)
    mock_check_conflict.assert_called_once()
    mock_create_reservation.assert_called_once()


@pytest.mark.asyncio
async def test_create_reservation_invalid_data(client):
    invalid_data = reservation_create.model_dump(mode="json")
    invalid_data["reservation_time"] = "invalid-date"

    response = client.post("/reservations/", json=invalid_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_delete_reservation_success(monkeypatch, mock_session, client):
    mock_delete_reservation = AsyncMock(return_value=True)
    monkeypatch.setattr(
        reservation_services, "delete_reservation_by_id", mock_delete_reservation
    )

    response = client.delete("/reservations/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Reservation deleted"}
    mock_delete_reservation.assert_called_once_with(1, mock_session)


@pytest.mark.asyncio
async def test_delete_reservation_not_found(monkeypatch, mock_session, client):
    mock_delete_reservation = AsyncMock(return_value=False)
    monkeypatch.setattr(
        reservation_services, "delete_reservation_by_id", mock_delete_reservation
    )

    response = client.delete("/reservations/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Reservation not found"}
    mock_delete_reservation.assert_called_once_with(1, mock_session)


@pytest.mark.asyncio
async def test_delete_reservation_invalid_id(client):
    response = client.delete("/reservations/invalid")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()
