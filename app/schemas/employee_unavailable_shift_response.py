from pydantic import BaseModel, Field


class EmployeeUnavailableShiftResponse(BaseModel):
    id: int = Field(gt=0)
    employee_id: int = Field(gt=0)
    shift_id: int = Field(gt=0)
