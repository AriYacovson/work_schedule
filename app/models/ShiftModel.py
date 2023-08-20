from sqlalchemy import Column, Integer, String, Time
from app.backend.database import Base


class ShiftModel(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
