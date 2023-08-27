from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.backend.database import Base


class EmployeeModel(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)

    assignments = relationship("EmployeeShiftAssignmentModel", back_populates="employee")
    unavailable_shifts = relationship(
        "EmployeeUnavailableShiftModel", back_populates="employee"
    )

