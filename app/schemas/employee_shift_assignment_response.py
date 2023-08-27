from pydantic import BaseModel
from datetime import date


class EmployeeShiftAssignmentResponse(BaseModel):
    id: int
    employee_id: int
    shift_id: int
    date: date
