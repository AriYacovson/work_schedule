from datetime import time

from pydantic import BaseModel


class ShiftTypeRequest(BaseModel):
    name: str
    start_time: time
    end_time: time
