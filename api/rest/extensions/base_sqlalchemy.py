from asyncio import current_task

from sqlalchemy import MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_scoped_session
from sqlalchemy.orm import sessionmaker

from rest.extensions.config_settings import config
import asyncpg  # noqa: F401


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


DeclarativeBase = declarative_base()
db = Database()

class Base(DeclarativeBase):
    __abstract__ = True

    @classmethod
    async def get_objects(cls):
        q = await db.session.execute(select(cls))
        objs = q.scalars().all()

        return objs

    @classmethod
    async def get_object(cls, object_id):
        q = await db.session.execute(select(cls).where(cls.id == object_id))
        obj = q.scalars().first()

        return obj

    @classmethod
    async def delete_object(cls, object_id):
        q = await db.session.execute(select(cls).where(cls.id == object_id))
        obj = q.scalars().first()

        if obj is None:
            return

        await db.session.delete(obj)
        await db.session.commit()

