from fastapi import APIRouter

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.get("/")
def get_reservation():
    return {"message": "No reservations right now"}