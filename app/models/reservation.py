from app.core.db import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    table_id = Column(Integer, ForeignKey("table.id"), nullable=False)
    table = relationship("Table", back_populates="reservations")