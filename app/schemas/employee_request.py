from pydantic import BaseModel, Field


class EmployeeRequest(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=100)
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    is_active: bool
    role: str = Field(min_length=3, max_length=100)