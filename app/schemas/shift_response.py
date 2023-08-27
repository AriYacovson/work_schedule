from datetime import time

from pydantic import BaseModel, Field


class ShiftResponse(BaseModel):
    id: int
    name: str
    start_time: time
    end_time: time
