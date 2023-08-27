from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.backend.database import get_db
from app.schemas.employee_unavailable_shift_response import (
    EmployeeUnavailableShiftResponse,
)
from app.schemas.employee_unavailable_shift_request import (
    EmployeeUnavailableShiftRequest,
)
from app.services import EmployeeUnavailableShiftService

router = APIRouter(
    prefix="/employee_unavailable_shift", tags=["employee_unavailable_shift"]
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[EmployeeUnavailableShiftResponse],
)
async def get_all_employee_unavailable_shifts(db: db_dependency):
    employee_unavailable_shifts = (
        EmployeeUnavailableShiftService.get_employee_unavailable_shifts(db)
    )
    if employee_unavailable_shifts:
        return employee_unavailable_shifts
    raise HTTPException(status_code=404, detail="EmployeeUnavailableShifts not found.")


@router.get("/{employee_unavailable_shift_id}", status_code=status.HTTP_200_OK)
async def get_employee_unavailable_shift(
    db: db_dependency, employee_unavailable_shift_id: int
):
    employee_unavailable_shift = (
        EmployeeUnavailableShiftService.get_employee_unavailable_shift_by_id(
            db, employee_unavailable_shift_id
        )
    )
    if employee_unavailable_shift:
        return employee_unavailable_shift
    raise HTTPException(status_code=404, detail="EmployeeUnavailableShift not found.")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeUnavailableShiftResponse,
)
async def create_employee_unavailable_shift(
    db: db_dependency,
    employee_unavailable_shift_request: EmployeeUnavailableShiftRequest,
):
    new_employee_unavailable_shift = (
        EmployeeUnavailableShiftService.create_employee_unavailable_shift(
            db, employee_unavailable_shift_request
        )
    )
    if new_employee_unavailable_shift:
        return new_employee_unavailable_shift
    raise HTTPException(
        status_code=400, detail="Failed to create a new employee_unavailable_shift."
    )


@router.post(
    "/from_text",
    status_code=status.HTTP_201_CREATED
)
async def create_employee_unavailable_shifts_from_text(
    db: db_dependency,
    employee_id: int,
    text: str
):
    new_employee_unavailable_shifts = (
        EmployeeUnavailableShiftService.create_employee_unavailable_shifts_from_text(
            db, employee_id, text
        )
    )
    if new_employee_unavailable_shifts:
        return status.HTTP_201_CREATED
    raise HTTPException(
        status_code=400, detail="Failed to create a new employee_unavailable_shift."
    )


@router.put(
    "/{employee_unavailable_shift_id}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeUnavailableShiftResponse,
)
async def update_employee_unavailable_shift(
    db: db_dependency,
    employee_unavailable_shift_id: int,
    employee_unavailable_shift_request: EmployeeUnavailableShiftRequest,
):
    updated_employee_unavailable_shift = (
        EmployeeUnavailableShiftService.update_employee_unavailable_shift(
            db, employee_unavailable_shift_id, employee_unavailable_shift_request
        )
    )
    if updated_employee_unavailable_shift:
        return updated_employee_unavailable_shift
    raise HTTPException(
        status_code=400, detail="Failed to update employee_unavailable_shift."
    )


@router.delete(
    "/{employee_unavailable_shift_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee_unavailable_shift(
    db: db_dependency, employee_unavailable_shift_id: int
):
    deleted_employee_unavailable_shift = (
        EmployeeUnavailableShiftService.delete_employee_unavailable_shift(
            db, employee_unavailable_shift_id
        )
    )
    if deleted_employee_unavailable_shift:
        return deleted_employee_unavailable_shift
    raise HTTPException(
        status_code=400, detail="Failed to delete employee_unavailable_shift."
    )
