from typing import Dict

from rest.extensions import db
from rest.factories.base_factory import (
    BaseFactory,
    ErrorCreateObject,
)
from rest.models import (
    Tag,
    Timer,
)
from sqlalchemy import select


class TimerFactory(BaseFactory[Timer]):

    class Meta:
        model = Timer

    async def create(self) -> Timer:
        return await self._create()

    @classmethod
    async def before_create(
        cls,
        data_for_create: Dict,
    ) -> Dict:
        data_for_create = await cls.set_tag_id(data_for_create)
        data_for_create = await cls.set_start_at(data_for_create)
        data_for_create = await cls.set_finish_at(data_for_create)

        return data_for_create

    @classmethod
    async def set_tag_id(
        cls,
        data_for_create: Dict,
    ) -> Dict:
        tag_id = data_for_create.get("tag_id")

        if tag_id is None:
            return data_for_create

        tag = await db.first(select(Tag).filter(Tag.id == tag_id))

        if tag is None:
            raise ErrorCreateObject("Тэг не существует")

        return data_for_create

    @classmethod
    async def set_start_at(
        cls,
        data_for_create: Dict,
    ) -> Dict:
        return data_for_create

    @classmethod
    async def set_finish_at(
        cls,
        data_for_create: Dict,
    ) -> Dict:
        return data_for_create

    @classmethod
    async def after_commit(
        cls,
        result_data: Timer,
    ) -> None:
        pass
