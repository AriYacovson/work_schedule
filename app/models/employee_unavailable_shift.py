from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.backend.database import Base


class EmployeeUnavailableShiftModel(Base):
    __tablename__ = "employee_unavailable_shifts"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    date = Column(Date, nullable=False)

    employee = relationship("EmployeeModel", back_populates="unavailable_shifts")
    shift = relationship("ShiftModel", back_populates="unavailable_employees")
