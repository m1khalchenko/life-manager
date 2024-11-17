from datetime import (
    datetime,
    timedelta,
)
from typing import Optional

from rest.schemas.base_schema import BaseSchema
from rest.schemas.tag import TagSchema


class CreateTimerSchema(BaseSchema):
    tag_id: Optional[int] = None
    finish_at: Optional[datetime] = None
    start_at: Optional[datetime] = None


class TimerSchema(CreateTimerSchema):
    id: int
    start_at: datetime
    tag: Optional[TagSchema] = None
    result_time: Optional[timedelta] = None

    class Config:
        orm_mode = True


class UpdateTimerSchema(CreateTimerSchema):
    pass
