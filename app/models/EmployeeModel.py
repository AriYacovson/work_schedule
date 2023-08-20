from sqlalchemy import Column, Integer, String, Boolean
from app.backend.database import Base


class EmployeeModel(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
