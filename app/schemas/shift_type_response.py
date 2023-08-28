from datetime import time

from pydantic import BaseModel


class ShiftTypeResponse(BaseModel):
    id: int
    name: str
    start_time: time
    end_time: time
