from datetime import time, date

from pydantic import BaseModel, Field


class ShiftResponse(BaseModel):
    id: int
    date: date
    name: str
    start_time: time
    end_time: time
