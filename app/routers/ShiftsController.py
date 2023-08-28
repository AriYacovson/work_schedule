from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from app.backend.database import get_db
from app.schemas.shift_request import ShiftRequest
from app.schemas.shift_response import ShiftResponse
from app.schemas.weekly_shift_request import WeeklyShiftRequest
from app.services import ShiftService

router = APIRouter(prefix="/shifts", tags=["shifts"])


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_shifts(db: db_dependency):
    return ShiftService.get_shifts(db)


@router.get("/{shift_id}", status_code=status.HTTP_200_OK)
async def get_shift(db: db_dependency, shift_id: int = Path(gt=0)):
    shift = ShiftService.get_shift_by_id(db, shift_id)
    if shift:
        return shift
    raise HTTPException(status_code=404, detail="ShiftModel not found.")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShiftResponse)
async def create_shift(db: db_dependency, shift_request: ShiftRequest):
    new_shift = ShiftService.create_shift(db, shift_request)
    if new_shift:
        return new_shift
    raise HTTPException(status_code=400, detail="Failed to create a new shift.")


@router.post("/generate_weekly_shifts", status_code=status.HTTP_201_CREATED)
async def generate_weekly_shifts(db: db_dependency, weekly_shift_request: WeeklyShiftRequest):
    ShiftService.generate_weekly_shifts(db, weekly_shift_request.start_date)
    return {"message": "Weekly shifts generated successfully."}





# @router.post("/generate_weekly_shifts/", status_code=status.HTTP_201_CREATED)
# async def generate_weekly_shifts(db: db_dependency, start_date: datetime.date):
#     # success = ShiftService.generate_weekly_shifts(db, start_date)
#     # if not success:
#     #     raise HTTPException(
#     #         status_code=400, detail="Failed to generate weekly shifts."
#     #     )
#     return True


@router.put("/{shift_id}", status_code=status.HTTP_200_OK, response_model=ShiftResponse)
async def update_shift(
    db: db_dependency, shift_request: ShiftRequest, shift_id: int = Path(gt=0)
):
    updated_shift = ShiftService.update_shift(db, shift_id, shift_request)
    if not updated_shift:
        raise HTTPException(
            status_code=404, detail="Shift not found or failed to update."
        )
    return updated_shift


@router.delete("/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shift(db: db_dependency, shift_id: int = Path(gt=0)):
    success = ShiftService.delete_shift(db, shift_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Shift not found or failed to delete."
        )
