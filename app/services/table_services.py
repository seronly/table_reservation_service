import logging
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Table
from app.schemas.table import TableCreate


logger = logging.getLogger(__name__)

async def create_table(table: TableCreate, session: AsyncSession) -> Table | None:
    table_db = Table(**table.model_dump())
    try:
        session.add(table_db)
        await session.commit()
        await session.refresh(table_db)
        return table_db
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        await session.rollback()
        return None

async def get_tables(session: AsyncSession) -> list[Table]:
    query = select(Table)
    result = await session.execute(query)
    return result.scalars().all()

async def get_table_by_id(id: int, session: AsyncSession) -> Table | None:
    query = select(Table).where(Table.id == id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def delete_table_by_id(id: int, session: AsyncSession) -> bool:
    table = await get_table_by_id(id, session)
    if not table:
        return False

    query = delete(Table).where(Table.id == id)
    await session.execute(query)
    await session.commit()
    return True