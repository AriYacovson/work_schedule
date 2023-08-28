import logging

from sqlalchemy.exc import SQLAlchemyError

from app.models import ShiftTypeModel
from app.schemas.shift_type_request import ShiftTypeRequest
from app.schemas.shift_type_response import ShiftTypeResponse

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_shift_types(db) -> list[ShiftTypeResponse]:
    try:
        return db.query(ShiftTypeModel).all()
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch all shift types: {e}")
        return []


def get_shift_type_by_id(db, shift_type_id: int) -> ShiftTypeResponse:
    try:
        return db.query(ShiftTypeModel).filter(ShiftTypeModel.id == shift_type_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Fails to fetch shift type with id {shift_type_id}: {e}")
        return None


def create_shift_type(db, shift_type_model: ShiftTypeRequest) -> ShiftTypeRequest:
    shift_type_model = ShiftTypeModel(**shift_type_model.model_dump())
    try:
        db.add(shift_type_model)
        db.commit()
        db.refresh(shift_type_model)
        return shift_type_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to create shift type: {e}")
        db.rollback()
        return None


def update_shift_type(db, shift_type_request: ShiftTypeRequest, shift_type_id: int) -> ShiftTypeResponse:
    shift_type_model = get_shift_type_by_id(db, shift_type_id)
    if not shift_type_model:
        return None
    try:
        shift_type_model.name = shift_type_request.name
        shift_type_model.start_time = shift_type_request.start_time
        shift_type_model.end_time = shift_type_request.end_time
        db.add(shift_type_model)
        db.commit()
        db.refresh(shift_type_model)
        return shift_type_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to update shift type: {e}")
        db.rollback()
        return None


def delete_shift_type(db, shift_type_id: int) -> bool:
    try:
        result = db.query(ShiftTypeModel).filter(ShiftTypeModel.id == shift_type_id).delete()
        if not result:
            return False
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Failed to delete shift type: {e}")
        db.rollback()
        return False
