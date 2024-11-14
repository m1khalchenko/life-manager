import sqlalchemy as sa
from rest.extensions import Base


class Tag(Base):
    __tablename__ = 'tag'

    name = sa.Column(sa.String, nullable=False)
