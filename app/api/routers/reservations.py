from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import create_session
from app.schemas.reservation import Reservation, ReservationCreate
from app.services import reservation_services as rs, table_services

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.get("/")
async def get_reservation(session: AsyncSession = Depends(create_session)) -> list[Reservation]:
    reservations = await rs.get_reservations(session)
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservations not found"
        )
    return reservations

@router.post("/")
async def create_reservation(reservation: ReservationCreate, session: AsyncSession = Depends(create_session)) -> Reservation:
    is_table_exists = await table_services.get_table_by_id(reservation.table_id, session)
    if not is_table_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Table with id {reservation.table_id} not found"
        )
    is_time_conflicts = await rs.check_reservation_conflict(
        reservation.reservation_time,
        reservation.duration_minutes,
        reservation.table_id,
        session
    )
    if is_time_conflicts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time conflicts. This table is already reserved at this time"
        )
    reservation = await rs.create_reservation(reservation, session)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservation not created"
        )
    return reservation

@router.delete("/{id}")
async def delete_reservation(id: int, session: AsyncSession = Depends(create_session)) -> JSONResponse:
    result = await rs.delete_reservation_by_id(id, session)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Reservation deleted"}
    )