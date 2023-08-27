from app.models.employee_shift_assignment import EmployeeShiftAssignmentModel
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
import logging

from app.schemas.employee_shift_assignment_request import EmployeeShiftAssignmentRequest
from app.schemas.employee_shift_assignment_response import (
    EmployeeShiftAssignmentResponse,
)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_employee_shift_assignments(db):
    try:
        return db.query(EmployeeShiftAssignmentModel).all()
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch all assignments: {e}")
        return None


def get_employee_shift_assignment_by_id(db, employee_shift_assignment_id: int):
    try:
        return (
            db.query(EmployeeShiftAssignmentModel)
            .filter(EmployeeShiftAssignmentModel.id == employee_shift_assignment_id)
            .first()
        )
    except SQLAlchemyError as e:
        logger.error(
            f"Failed to fetch assignment with id {employee_shift_assignment_id}: {e}"
        )
        return None


def get_employee_shift_assignments_by_employee_id(db, employee_id: int):
    try:
        return (
            db.query(EmployeeShiftAssignmentModel)
            .filter(EmployeeShiftAssignmentModel.employee_id == employee_id)
            .all()
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch assignment with employee id {employee_id}: {e}")
        return None


def get_employee_shift_assignments_by_shift_id(db, shift_id: int):
    try:
        return (
            db.query(EmployeeShiftAssignmentModel)
            .filter(EmployeeShiftAssignmentModel.shift_id == shift_id)
            .all()
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch assignment with shift id {shift_id}: {e}")
        return None


def get_employee_shift_assignments_by_date(
    db, date: date
) -> list[EmployeeShiftAssignmentResponse]:
    try:
        return (
            db.query(EmployeeShiftAssignmentModel)
            .filter(EmployeeShiftAssignmentModel.date == date)
            .all()
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch assignment with date {date}: {e}")
        return None


def create_employee_shift_assignment(
    db, employee_shift_assigment_request: EmployeeShiftAssignmentRequest
) -> EmployeeShiftAssignmentResponse:
    employee_shift_assignment_model = EmployeeShiftAssignmentModel(
        **employee_shift_assigment_request.model_dump()
    )
    try:
        db.add(employee_shift_assignment_model)
        db.commit()
        db.refresh(employee_shift_assignment_model)
        return employee_shift_assignment_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to create assignment: {e}")
        db.rollback()
        return None


def update_employee_shift_assignment(
    db,
    assignment_id: int,
    employee_shift_assigment_request: EmployeeShiftAssignmentRequest,
) -> EmployeeShiftAssignmentModel:
    employee_shift_assignment_model = get_employee_shift_assignment_by_id(
        db, assignment_id
    )
    if not employee_shift_assignment_model:
        return None
    try:
        employee_shift_assignment_model.employee_id = (
            employee_shift_assigment_request.employee_id
        )
        employee_shift_assignment_model.shift_id = (
            employee_shift_assigment_request.shift_id
        )
        employee_shift_assignment_model.date = employee_shift_assigment_request.date
        db.add(employee_shift_assignment_model)
        db.commit()
        db.refresh(employee_shift_assignment_model)
        return employee_shift_assignment_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to update assignment with id {assignment_id}: {e}")
        db.rollback()
        return None


def delete_employee_shift_assignment(db, assignment_id: int) -> bool:
    try:
        result = (
            db.query(EmployeeShiftAssignmentModel)
            .filter(EmployeeShiftAssignmentModel.id == assignment_id)
            .delete()
        )
        if not result:
            return False
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Failed to delete assignment with id {assignment_id}: {e}")
        db.rollback()
        return False
