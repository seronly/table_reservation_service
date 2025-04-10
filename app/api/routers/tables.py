from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import create_session
from app.schemas.table import TableCreate, Table
from app.services import table_services

router = APIRouter(prefix="/tables", tags=["tables"])

@router.get("/")
async def get_table(session: AsyncSession = Depends(create_session)) -> list[Table] | dict:
    tables = await table_services.get_tables(session)
    if not tables:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tables not found"
        )
    return tables

@router.post("/")
async def create_table(table: TableCreate, session: AsyncSession = Depends(create_session)) -> TableCreate:
    db_table = await table_services.create_table(table, session)
    if not db_table:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Table not created"
        )
    return db_table

@router.delete("/{id}")
async def delete_table(id: int, session: AsyncSession = Depends(create_session)) -> JSONResponse:
    table_deleted = await table_services.delete_table_by_id(id, session)
    if not table_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id {id} not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Table with id {id} deleted"}
    )