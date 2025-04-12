from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ReservationBase(BaseModel):
    """
        This schema is base for a reservation.
    """
    customer_name: str = Field(min_length=1, max_length=100)
    reservation_time: datetime = Field(default_factory=datetime.now)
    duration_minutes: int = Field(ge=1)
    table_id: int

class ReservationCreate(ReservationBase):
    """
        This schema is used to create a reservation.
    """
    pass

class Reservation(ReservationBase):
    """
        This schema is used to return a reservation.
    """
    model_config = ConfigDict(from_attributes=True)
    id: int