from app.models.employee_unavailable_shift import EmployeeUnavailableShiftModel
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
import logging

from app.schemas.employee_unavailable_shift_request import (
    EmployeeUnavailableShiftRequest,
)
from app.schemas.employee_unavailable_shift_response import (
    EmployeeUnavailableShiftResponse,
)

# from app.schemas.EmployeeShiftAssignmentRequest import EmployeeShiftAssignmentRequest
# from app.schemas.EmployeeShiftAssignmentResponse import EmployeeShiftAssignmentResponse

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_employee_unavailable_shifts(db) -> list[EmployeeUnavailableShiftResponse]:
    try:
        return db.query(EmployeeUnavailableShiftModel).all()
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch all unavailable shifts: {e}")
        return None


def get_employee_unavailable_shift_by_id(
    db, employee_unavailable_shift_id: int
) -> EmployeeUnavailableShiftResponse:
    try:
        return (
            db.query(EmployeeUnavailableShiftModel)
            .filter(EmployeeUnavailableShiftModel.id == employee_unavailable_shift_id)
            .first()
        )
    except SQLAlchemyError as e:
        logger.error(
            f"Failed to fetch unavailable shift with id {employee_unavailable_shift_id}: {e}"
        )
        return None


def create_employee_unavailable_shift(
    db, employee_unavailable_shift: EmployeeUnavailableShiftRequest
) -> EmployeeUnavailableShiftResponse:
    employee_unavailable_shift_model = EmployeeUnavailableShiftModel(
        **employee_unavailable_shift.model_dump()
    )
    try:
        db.add(employee_unavailable_shift_model)
        db.commit()
        db.refresh(employee_unavailable_shift_model)
        return employee_unavailable_shift_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to create unavailable shift: {e}")
        return None


def update_employee_unavailable_shift(
    db, employee_unavailable_shift_id: int, employee_unavailable_shift_request: EmployeeUnavailableShiftRequest
) -> EmployeeUnavailableShiftResponse:
    employee_unavailable_shift_model = get_employee_unavailable_shift_by_id(db, employee_unavailable_shift_id)
    if employee_unavailable_shift_model:
        try:
            employee_unavailable_shift_model.shift_id = employee_unavailable_shift_request.shift_id
            employee_unavailable_shift_model.employee_id = employee_unavailable_shift_request.employee_id
            employee_unavailable_shift_model.date = employee_unavailable_shift_request.date
            db.commit()
            db.refresh(employee_unavailable_shift_model)
            return employee_unavailable_shift_model
        except SQLAlchemyError as e:
            logger.error(f"Failed to update unavailable shift: {e}")
            db.rollback()
            return None
    return None


def delete_employee_unavailable_shift(db, employee_unavailable_shift_id: int):
    employee_unavailable_shift_model = get_employee_unavailable_shift_by_id(
        db, employee_unavailable_shift_id
    )
    if employee_unavailable_shift_model:
        try:
            db.delete(employee_unavailable_shift_model)
            db.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Failed to delete unavailable shift: {e}")
            db.rollback()
            return False
    return False
