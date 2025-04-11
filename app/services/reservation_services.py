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