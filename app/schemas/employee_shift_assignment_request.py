from pydantic import BaseModel, Field
from datetime import date


class EmployeeShiftAssignmentRequest(BaseModel):
    employee_id: int = Field(gt=0)
    shift_id: int = Field(gt=0)
    date: date
    