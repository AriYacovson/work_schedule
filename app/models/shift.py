from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship

from app.backend.database import Base


class ShiftModel(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    assignments = relationship("EmployeeShiftAssignmentModel", back_populates="shift")
    unavailable_employees = relationship(
        "EmployeeUnavailableShiftModel", back_populates="shift"
    )