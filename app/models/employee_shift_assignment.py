from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.database import Base


class EmployeeShiftAssignmentModel(Base):
    __tablename__ = "employee_shift_assignments"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    date = Column(Date, nullable=False)

    employee = relationship("EmployeeModel", back_populates="assignments")
    shift = relationship("ShiftModel", back_populates="assignments")





