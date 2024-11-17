from typing import (
    Dict,
    Generic,
    Optional,
    TypeVar,
)

from rest.extensions import (
    Base,
    db,
)
from sqlalchemy.ext.asyncio import AsyncSession

TypeBaseFactory = TypeVar("TypeBaseFactory", bound="BaseFactory")
TypeBaseModel = TypeVar("TypeBaseModel", bound=Base)


class ErrorCreateObject(Exception):
    pass


class BaseFactory(Generic[TypeBaseModel]):
    class Meta:
        model = Base

    def __init__(
        self,
        data_for_create: Dict,
        commit_model: bool = True,
        session: Optional[AsyncSession] = None,
    ) -> None:
        self._commit_model = commit_model
        self._session = session or db.session
        self._data_for_create: Dict = data_for_create or {}

    async def _create(self) -> TypeBaseModel:
        return await self._create_instance()

    async def _create_instance(self) -> TypeBaseModel:
        data_for_create = await self.before_create(
            data_for_create=self._data_for_create,
        )

        obj = self.Meta.model(**data_for_create)

        self._session.add(obj)
        await self._commit()

        await self.after_commit(
            result_data=obj,
        )

        return obj

    @classmethod
    async def before_create(
        cls,
        data_for_create: Dict,
    ) -> Dict:
        raise Exception

    @classmethod
    async def after_commit(
        cls,
        result_data: TypeBaseModel,
    ) -> None:
        raise Exception

    async def _commit(self) -> None:
        if self._commit_model:
            await self._session.commit()
