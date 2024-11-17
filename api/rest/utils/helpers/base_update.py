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

TypeBaseModel = TypeVar("TypeBaseModel", bound=Base)


class ErrorUpdateObject(Exception):
    pass


class BaseUpdate(Generic[TypeBaseModel]):
    def __init__(
        self,
        instance: TypeBaseModel,
        data_for_update: Dict,
        session: Optional[AsyncSession] = None,
    ):
        self.instance = instance
        self.data_for_update = data_for_update
        self._session = session or db.session

    async def update(self) -> TypeBaseModel:
        await self._update()
        await self._session.commit()

        return self.instance

    async def _update(self) -> None:
        raise Exception
