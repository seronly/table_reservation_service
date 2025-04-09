from fastapi import APIRouter

router = APIRouter(prefix="/tables", tags=["tables"])

@router.get("/")
def get_table():
    return {"message": "No tables right now"}