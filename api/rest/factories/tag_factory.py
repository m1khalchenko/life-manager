from typing import Dict

from rest.factories.base_factory import BaseFactory
from rest.models import Tag


class TagFactory(BaseFactory[Tag]):
    class Meta:
        model = Tag

    async def create(self) -> Tag:
        return await self._create()

    @classmethod
    async def before_create(
        cls,
        data_for_create: Dict,
    ) -> Dict:
        return data_for_create

    @classmethod
    async def after_commit(
        cls,
        result_data: Tag,
    ) -> None:
        pass
