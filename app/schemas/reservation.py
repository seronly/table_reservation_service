from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ReservationBase(BaseModel):
    customer_name: str
    reservation_time: datetime
    duration_minutes: int
    table_id: int

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int