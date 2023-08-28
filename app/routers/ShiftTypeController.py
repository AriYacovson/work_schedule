from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.backend.database import get_db
from app.schemas.shift_type_request import ShiftTypeRequest
from app.services import ShiftTypeService

router = APIRouter(prefix="/shift_type", tags=["shift_type"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_shift_types(db: db_dependency):
    shift_types = ShiftTypeService.get_shift_types(db)
    if shift_types:
        return shift_types
    raise HTTPException(status_code=404, detail="Shift types not found.")


@router.get("/{shift_type_id}", status_code=status.HTTP_200_OK)
async def get_shift_type(db: db_dependency, shift_type_id: int):
    shift = ShiftTypeService.get_shift_type_by_id(db, shift_type_id)
    if shift:
        return shift
    raise HTTPException(status_code=404, detail="Shift type not found.")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_shift_type(db: db_dependency, shift_type_request: ShiftTypeRequest):
    new_shift_type = ShiftTypeService.create_shift_type(db, shift_type_request)
    if new_shift_type:
        return new_shift_type
    raise HTTPException(status_code=400, detail="Failed to create a new shift type.")


@router.put("/{shift_type_id}", status_code=status.HTTP_200_OK)
async def update_shift_type(
    db: db_dependency, shift_type_request: ShiftTypeRequest, shift_type_id: int
):
    updated_shift_type = ShiftTypeService.update_shift_type(
        db, shift_type_request, shift_type_id
    )
    if updated_shift_type:
        return updated_shift_type
    raise HTTPException(status_code=400, detail="Failed to update shift type.")


@router.delete("/{shift_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shift_type(db: db_dependency, shift_type_id: int):
    success = ShiftTypeService.delete_shift_type(db, shift_type_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete shift type.")

