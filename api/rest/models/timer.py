from datetime import (
    datetime,
    timedelta,
)
from typing import List

import sqlalchemy as sa
from rest.extensions import (
    Base,
    db,
)
from sqlalchemy import select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    relationship,
    selectinload,
)


class Timer(Base):
    __tablename__ = 'timer'

    start_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    finish_at = sa.Column(sa.DateTime)
    tag_id = sa.Column(sa.Integer, sa.ForeignKey('tag.id', ondelete='SET NULL'))
    tag = relationship("Tag", foreign_keys=[tag_id])

    @hybrid_property
    def result_time(self) -> timedelta:
        if self.finish_at is None:
            return datetime.utcnow() - self.start_at
        return self.finish_at - self.start_at  # type: ignore

    @classmethod
    async def get_objects(cls) -> List["Timer"]:
        objs = await db.all(
            select(cls)
            .options(selectinload(cls.tag)),
        )

        return objs

    @classmethod
    async def get_object(cls, object_id: int) -> "Timer":
        obj = await db.first(
            select(cls)
            .options(selectinload(cls.tag))
            .where(cls.id == object_id),
        )

        return obj
