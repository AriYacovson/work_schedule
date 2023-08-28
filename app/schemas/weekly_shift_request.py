from datetime import date

from pydantic import BaseModel


class WeeklyShiftRequest(BaseModel):
    start_date: date
