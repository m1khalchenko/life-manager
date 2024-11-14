from datetime import datetime, tzinfo

from pydantic import ValidationError, BaseModel
from sqlalchemy import select

from rest.factories.base_factory import BaseFactory
from rest.models import Timer, Tag


class TagFactory(BaseFactory[Tag]):
    class Meta:
        model = Tag

    async def create(self):
        return await self._create()

    async def before_create(
        self,
        data_for_create: BaseModel,
    ) -> BaseModel:
            return data_for_create

    async def after_create(
        self,
        result_data: Tag,
    ) -> Tag:
        pass