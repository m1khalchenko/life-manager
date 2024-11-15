from datetime import datetime, tzinfo

from pydantic import ValidationError, BaseModel
from sqlalchemy import select

from rest.factories.base_factory import BaseFactory
from rest.models import Timer, Tag


class TimerFactory(BaseFactory[Timer]):
    class Meta:
        model = Timer

    async def create(self):
        return await self._create()

    async def before_create(
        self,
        data_for_create: BaseModel,
    ) -> BaseModel:
        data_for_create = await self.set_tag_id(data_for_create)

        return data_for_create

    async def set_tag_id(self, data_for_create: BaseModel) -> BaseModel:
        tag_id = data_for_create.tag_id

        if tag_id is None:
            return data_for_create

        q = await self._session.execute(select(Tag).filter(Tag.id == tag_id))
        tag = q.scalars().first()

        if tag is None:
           raise ValidationError("Тэг не существует")

        return data_for_create

    async def after_create(
        self,
        result_data: Timer,
    ):
        pass