from datetime import datetime, timedelta
import logging
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Reservation
from app.schemas.reservation import ReservationCreate

logger = logging.getLogger(__name__)

async def create_reservation(reservation: ReservationCreate, session: AsyncSession) -> Reservation | None:
    reservation_db = Reservation(**reservation.model_dump())
    try:
        session.add(reservation_db)
        await session.commit()
        await session.refresh(reservation_db)
        return reservation_db
    except Exception as e:
        logger.error(f"Error creating reservation: {e}")
        await session.rollback()
        return None

async def get_reservations(session: AsyncSession) -> list[Reservation]:
    query = select(Reservation)
    result = await session.execute(query)
    return result.scalars().all()

async def get_reservation_by_id(id: int, session: AsyncSession) -> Reservation | None:
    query = select(Reservation).where(Reservation.id == id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def delete_reservation_by_id(id: int, session: AsyncSession) -> bool:
    reservation = await get_reservation_by_id(id, session)
    logger.warning(f"Reservation to delete: {reservation}")
    if not reservation:
        return False

    query = delete(Reservation).where(Reservation.id == id)
    await session.execute(query)
    await session.commit()
    return True


async def check_reservation_conflict(
    new_reservation_time: datetime,
    new_duration_minutes: int,
    new_table_id: int,
    session: AsyncSession
) -> bool:
    """
    Checks if there is a conflict for a new reservation on a table.
    Returns True if there is an overlap, else False.
    """
    new_reservation_time = new_reservation_time.replace(tzinfo=None)
    query = select(Reservation).where(Reservation.table_id == new_table_id).filter(
         new_reservation_time <= (
            Reservation.reservation_time + (Reservation.duration_minutes * timedelta(minutes=1))
        ),
        Reservation.reservation_time <= (
            new_reservation_time + timedelta(minutes=new_duration_minutes)
        )
    )
    conflicting_reservations = await session.execute(query)
    conflicting_reservations = conflicting_reservations.scalars().all()
    return len(conflicting_reservations) > 0