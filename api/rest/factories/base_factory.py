from typing import TypeVar, Generic, Any, Optional

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from rest.extensions import Base, db

TypeBaseFactory = TypeVar("TypeBaseFactory", bound="BaseFactory")
TypeBaseModel = TypeVar("TypeBaseModel", bound=Base)


class BaseFactory(Generic[TypeBaseModel]):
    class Meta:
        model = Base

    def __init__(
        self,
        data_for_create: BaseModel,
        commit_model: bool = True,
        session: Optional[AsyncSession] = None,
    ) -> None:
        self._commit_model = commit_model
        self._session = session or db.session
        self._data_for_create = data_for_create or {}


    async def _create(self):
        return await self._create_instance()

    async def _create_instance(self):
        data_for_create = await self.before_create(
            data_for_create=self._data_for_create
        )

        object = self.Meta.model(**data_for_create.dict())

        self._session.add(object)
        await self._commit()

        await self.after_create(
            result_data=object
        )

        return object

    async def before_create(
        self,
        data_for_create: BaseModel,
    ):
        raise Exception

    async def after_create(
        self,
        result_data: TypeBaseModel,
    ):
        raise Exception

    async def _commit(self):
        if self._commit_model:
            await self._session.commit()