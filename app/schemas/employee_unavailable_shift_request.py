from pydantic import BaseModel, Field


class EmployeeUnavailableShiftRequest(BaseModel):
    employee_id: int = Field(gt=0)
    shift_id: int = Field(gt=0)
