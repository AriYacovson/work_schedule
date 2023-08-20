from datetime import time
from pydantic import BaseModel, Field


class ShiftRequest(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    start_time: time
    end_time: time

