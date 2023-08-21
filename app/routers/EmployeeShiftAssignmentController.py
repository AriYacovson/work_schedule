from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status
from datetime import date

from app.backend.database import get_db

from app.schemas.EmployeeShiftAssignmentRequest import EmployeeShiftAssignmentRequest
from app.schemas.EmployeeShiftAssignmentResponse import EmployeeShiftAssignmentResponse
from app.services import EmployeeShiftAssignmentService


router = APIRouter(prefix="/employee_shift_assignment", tags=["employee_shift_assignment"])


db_dependency = Annotated[Session, Depends(get_db)]


# @router.get("/", status_code=status.HTTP_200_OK, response_model=list[EmployeeShiftAssignmentResponse])
# async def get_employee_shift_assignments(db: db_dependency):
#     employee_shift_assignments = EmployeeShiftAssignmentService.get_employee_shift_assignments(db)
#     if employee_shift_assignments:
#         return employee_shift_assignments
#     raise HTTPException(status_code=404, detail="EmployeeShiftAssignments not found.")


@router.get("/{employee_shift_assignment_id}", status_code=status.HTTP_200_OK)
async def get_employee_shift_assignment(db: db_dependency, employee_shift_assignment_id: int = Path(gt=0)):
    employee_shift_assignment = EmployeeShiftAssignmentService.get_employee_shift_assignment_by_id(db, employee_shift_assignment_id)
    if employee_shift_assignment:
        return employee_shift_assignment
    raise HTTPException(status_code=404, detail="EmployeeShiftAssignment not found.")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[EmployeeShiftAssignmentResponse])
async def get_employee_shift_assignments(db: db_dependency, date: date | None = None):
    if date:
        employee_shift_assignments = EmployeeShiftAssignmentService.get_employee_shift_assignments_by_date(db, date)
    else:
        employee_shift_assignments = EmployeeShiftAssignmentService.get_employee_shift_assignments(db)
    if employee_shift_assignments:
        return employee_shift_assignments
    raise HTTPException(status_code=404, detail="EmployeeShiftAssignments not found.")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeShiftAssignmentResponse)
async def create_employee_shift_assignment(db: db_dependency, employee_shift_assignment_request: EmployeeShiftAssignmentRequest):
    new_employee_shift_assignment = EmployeeShiftAssignmentService.create_employee_shift_assignment(db, employee_shift_assignment_request)
    if new_employee_shift_assignment:
        return new_employee_shift_assignment
    raise HTTPException(status_code=400, detail="Failed to create a new employee_shift_assignment.")


@router.put("/", status_code=status.HTTP_200_OK, response_model=EmployeeShiftAssignmentResponse)
async def update_employee_shift_assignment(db: db_dependency, employee_shift_assignment_request: EmployeeShiftAssignmentRequest):
    updated_employee_shift_assignment = EmployeeShiftAssignmentService.update_employee_shift_assignment(db, employee_shift_assignment_request)
    if updated_employee_shift_assignment:
        return updated_employee_shift_assignment
    raise HTTPException(status_code=404, detail="EmployeeShiftAssignment not found or failed to update.")


@router.delete("/{employee_shift_assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_shift_assignment(db: db_dependency, employee_shift_assignment_id: int = Path(gt=0)):
    success = EmployeeShiftAssignmentService.delete_employee_shift_assignment(db, employee_shift_assignment_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="EmployeeShiftAssignment not found or failed to delete."
        )
