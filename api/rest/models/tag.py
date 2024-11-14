from rest.extensions import Base
import sqlalchemy as sa


class Tag(Base):
    __tablename__ = 'tag'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
