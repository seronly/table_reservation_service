from fastapi import APIRouter
from . import tables, reservations

api_router = APIRouter()
api_router.include_router(tables.router)
api_router.include_router(reservations.router)