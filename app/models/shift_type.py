from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship

from app.backend.database import Base


class ShiftTypeModel(Base):
    __tablename__ = "shift_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    shifts = relationship("ShiftModel", back_populates="shift_type")


