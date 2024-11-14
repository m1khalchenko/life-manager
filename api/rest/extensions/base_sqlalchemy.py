from typing import List

import asyncpg  # noqa: F401
import sqlalchemy as sa
from rest.extensions.config_settings import config
from sqlalchemy import (
    Executable,
    MetaData,
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:

    def __init__(self) -> None:
        self.engine = self.create_async_engine()
        session = self.create_async_session()
        self.session = session()

    def create_async_session(self) -> sessionmaker:
        session = sessionmaker(  # type: ignore
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        return session

    @classmethod
    def create_async_engine(cls) -> AsyncEngine:
        engine = create_async_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
        return engine

    @property
    def metadata(self) -> MetaData:
        return Base.metadata

    async def all(self, query: Executable) -> "Base":
        q = await self.session.execute(query)

        return q.scalars().all()

    async def first(self, query: Executable) -> "Base":
        q = await self.session.execute(query)

        return q.scalars().first()


DeclarativeBase = declarative_base()
db = Database()


class Base(DeclarativeBase):  # type: ignore
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True)

    @classmethod
    async def get_objects(cls) -> List["Base"]:
        objs = await db.all(select(cls))

        return objs

    @classmethod
    async def get_object(cls, object_id: int) -> "Base":
        obj = await db.first(select(cls).where(cls.id == object_id))

        return obj

    @classmethod
    async def delete_object(cls, object_id: int) -> None:
        obj = await db.first(select(cls).where(cls.id == object_id))

        if obj is None:
            return

        await db.session.delete(obj)
        await db.session.commit()
