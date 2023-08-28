import re
from datetime import date, time
from pydantic import BaseModel, Field, validator, field_validator


class ShiftRequest(BaseModel):
    date: date
    name: str = Field(min_length=3, max_length=100)
    start_time: time
    end_time: time

    @field_validator('start_time', 'end_time', mode='before')
    def check_time_format(cls, v):
        if isinstance(v, time):
            return v

        if re.match(r'^\d{2}:\d{2}$', v):
            hour, minute = map(int, v.split(':'))
            return time(hour=hour, minute=minute)

        raise ValueError('Invalid time format')

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Morning Shift",
                    "start_time": "08:00",
                    "end_time": "16:00"
                }
            ]
        }
    }

