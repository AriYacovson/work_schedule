from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.backend.database import get_db
from app.schemas.employee_request import EmployeeRequest
from app.schemas.employee_response import EmployeeResponse
from app.services import EmployeeService

router = APIRouter(prefix="/employee", tags=["employee"])


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_employees(db: db_dependency):
    return EmployeeService.get_employees(db)


@router.get("/{employee_id}", status_code=status.HTTP_200_OK)
async def get_employee(db: db_dependency, employee_id: int = Path(gt=0)):
    employee = EmployeeService.get_employee_by_id(db, employee_id)
    if employee:
        return employee
    raise HTTPException(status_code=404, detail="Employee not found.")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(db: db_dependency, employee_request: EmployeeRequest):
    new_employee = EmployeeService.create_employee(db, employee_request)
    if new_employee:
        return new_employee
    raise HTTPException(status_code=400, detail="Failed to create a new employee.")


@router.put(
    "/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse
)
async def update_employee(
    db: db_dependency, employee_request: EmployeeRequest, employee_id: int = Path(gt=0)
):
    updated_employee = EmployeeService.update_employee(
        db, employee_id, employee_request
    )
    if updated_employee:
        return updated_employee
    raise HTTPException(
        status_code=404, detail="Employee not found or failed to update."
    )


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(db: db_dependency, employee_id: int = Path(gt=0)):
    success = EmployeeService.delete_employee(db, employee_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Employee not found or failed to delete."
        )
