from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel

from rest.schemas.tag import TagSchema


class CreateTimerSchema(BaseModel):
    tag_id: Optional[int] = None


class TimerSchema(CreateTimerSchema):
    id: int
    start_at: datetime
    finish_at: Optional[datetime] = None
    tag: Optional[TagSchema] = None
    result_time: Optional[timedelta] = None

    class Config:
        orm_mode = True