from datetime import timedelta, datetime, time

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


# def generate_weekly_shifts(db, start_date):
#     shift_types = [("morning", timedelta(hours=7), timedelta(hours=15)),
#                    ("afternoon", timedelta(hours=15), timedelta(hours=23)),
#                    ("night", timedelta(hours=23), timedelta(hours=7))]
#     for day in range(7):
#         current_date = start_date + timedelta(days=day)
#         for name, start, end in shift_types:
#             shift_start_time = (datetime.combine(current_date, time(0, 0) + start).time())
#             if end.days == 1:
#                 shift_end_time = (end - timedelta(days=1)).time()
#                 shift_date = current_date + timedelta(days=1)
#             else:
#                 shift_end_time = end.time()
#                 shift_date = current_date
#
#             new_shift = ShiftModel(name=name, start_time=shift_start_time, end_time=shift_end_time, date=shift_date)
#             db.add(new_shift)
#     db.commit()
#     return True

def generate_weekly_shifts(db, start_date):
    for i in range(7):
        new_shift = ShiftModel(name="morning", start_time=time(7, 0), end_time=time(15, 0),
                               date=start_date + timedelta(days=i))
        db.add(new_shift)
        new_shift = ShiftModel(name="afternoon", start_time=time(15, 0), end_time=time(23, 0),
                               date=start_date + timedelta(days=i))
        db.add(new_shift)
        new_shift = ShiftModel(name="night", start_time=time(23, 0), end_time=time(7, 0),
                               date=start_date + timedelta(days=i))
        db.add(new_shift)
    db.commit()
    return True


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


