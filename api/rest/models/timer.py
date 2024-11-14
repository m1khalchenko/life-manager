from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, session

from rest.extensions import Base, db
import sqlalchemy as sa


class Timer(Base):
    __tablename__ = 'timer'

    id = sa.Column(sa.Integer, primary_key=True)
    start_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    finish_at = sa.Column(sa.DateTime)
    tag_id = sa.Column(sa.Integer, sa.ForeignKey('tag.id'))
    tag = relationship("Tag", foreign_keys=[tag_id])

    @hybrid_property
    def result_time(self) -> timedelta:
        if self.finish_at is None:
            return datetime.utcnow() - self.start_at
        return self.finish_at - self.start_at  # type: ignore
