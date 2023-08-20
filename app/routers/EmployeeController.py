from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.backend.database import get_db
from app.models.EmployeeModel import EmployeeModel
from app.schemas.EmployeeRequest import EmployeeRequest
from app.schemas.EmployeeResponse import EmployeeResponse

router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_employees(db: db_dependency):
    return db.query(EmployeeModel).all()


@router.get("/{employee_id}", status_code=status.HTTP_200_OK)
async def get_employee(db: db_dependency,
                       employee_id: int = Path(gt=0)):
    employee_model = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not employee_model:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return employee_model


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(db: db_dependency, employee_request: EmployeeRequest):
    employee_model = EmployeeModel(**employee_request.model_dump())
    db.add(employee_model)
    db.commit()
    db.refresh(employee_model)
    return employee_model


@router.put("/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def update_employee(db: db_dependency,
                          employee_request: EmployeeRequest,
                          employee_id: int = Path(gt=0)):
    employee_model = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not employee_model:
        raise HTTPException(status_code=404, detail="Employee not found.")
    employee_model.username = employee_request.username
    employee_model.first_name = employee_request.first_name
    employee_model.last_name = employee_request.last_name
    employee_model.is_active = employee_request.is_active
    employee_model.role = employee_request.role

    db.add(employee_model)
    db.commit()


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(db: db_dependency,
                          employee_id: int = Path(gt=0)):
    result = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).delete()

    # If no rows were deleted, then the employee did not exist.
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found.")

    db.commit()






