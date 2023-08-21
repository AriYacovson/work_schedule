from sqlalchemy.exc import SQLAlchemyError

from app.models.EmployeeModel import EmployeeModel
from app.schemas.EmployeeRequest import EmployeeRequest
from app.schemas.EmployeeResponse import EmployeeResponse

import logging


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_employees(db) -> list[EmployeeModel]:
    try:
        return db.query(EmployeeModel).all()
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch all employees: {e}")
        return None


def get_employee_by_id(db, employee_id: int) -> EmployeeModel:
    try:
        return db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Fails to fetch employee with id {employee_id}: {e}")
        return None


def create_employee(db, employee_request: EmployeeRequest) -> EmployeeResponse:
    employee_model = EmployeeModel(**employee_request.model_dump())
    try:
        db.add(employee_model)
        db.commit()
        db.refresh(employee_model)
        return employee_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to create employee: {e}")
        db.rollback()
        return None


def update_employee(db, employee_id: int, employee_request: EmployeeRequest) -> EmployeeResponse:
    employee_model = get_employee_by_id(db, employee_id)
    if not employee_model:
        return None
    try:
        employee_model.email = employee_request.email
        employee_model.username = employee_request.username
        employee_model.first_name = employee_request.first_name
        employee_model.last_name = employee_request.last_name
        employee_model.is_active = employee_request.is_active
        employee_model.role = employee_request.role
        db.add(employee_model)
        db.commit()
        db.refresh(employee_model)
        return employee_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to update employee with id {employee_id}: {e}")
        db.rollback()
        return None


def delete_employee(db, employee_id: int) -> bool:
    try:
        result = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).delete()
        if not result:
            return False
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Failed to delete employee with id {employee_id}: {e}")
        db.rollback()
        return False


