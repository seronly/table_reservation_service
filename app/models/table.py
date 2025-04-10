from app.core.db import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    reservations = relationship("Reservation", back_populates="table")