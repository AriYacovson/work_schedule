from sqlalchemy.exc import SQLAlchemyError

from app.models.shift import ShiftModel
from app.schemas.shift_request import ShiftRequest
from app.schemas.shift_response import ShiftResponse
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_shifts(db) -> list[ShiftModel]:
    try:
        return db.query(ShiftModel).all()
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch all shifts: {e}")
        return []


def get_shift_by_id(db, shift_id: int) -> ShiftModel:
    try:
        return db.query(ShiftModel).filter(ShiftModel.id == shift_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Fails to fetch shift with id {shift_id}: {e}")
        return None


def create_shift(db, shift_model: ShiftRequest) -> ShiftResponse:
    shift_model = ShiftModel(**shift_model.model_dump())
    try:
        db.add(shift_model)
        db.commit()
        db.refresh(shift_model)
        return shift_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to create shift: {e}")
        db.rollback()
        return None


def update_shift(db, shift_id: int, shift_request: ShiftRequest) -> ShiftResponse:
    shift_model = get_shift_by_id(db, shift_id)
    if not shift_model:
        return None
    try:
        shift_model.name = shift_request.name
        shift_model.start_time = shift_request.start_time
        shift_model.end_time = shift_request.end_time
        db.add(shift_model)
        db.commit()
        db.refresh(shift_model)
        return shift_model
    except SQLAlchemyError as e:
        logger.error(f"Failed to update shift with id {shift_id}: {e}")
        db.rollback()
        return None


def delete_shift(db, shift_id: int) -> bool:
    try:
        result = db.query(ShiftModel).filter(ShiftModel.id == shift_id).delete()
        if not result:
            return False
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Failed to delete shift with id {shift_id}: {e}")
        db.rollback()
        return False
