from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.database import Base


class ShiftModel(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    shift_type_id = Column(Integer, ForeignKey("shift_types.id"), nullable=False)
    date = Column(Date, nullable=False)

    assignments = relationship("EmployeeShiftAssignmentModel", back_populates="shift")
    unavailable_employees = relationship(
        "EmployeeUnavailableShiftModel", back_populates="shift"
    )
    shift_type = relationship("ShiftTypeModel", back_populates="shifts")
