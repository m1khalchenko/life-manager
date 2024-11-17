from rest.models import (
    Tag,
    Timer,
)
from rest.utils.helpers.base_update import (
    BaseUpdate,
    ErrorUpdateObject,
)


class TimerUpdate(BaseUpdate[Timer]):

    async def _update(self) -> None:
        await self._update_start_at()
        await self._update_finish_at()
        await self._update_tag_id()

    async def _update_start_at(self) -> None:
        start_at = self.data_for_update.get("start_at")

        if start_at is None:
            return

        self.instance.start_at = start_at

    async def _update_finish_at(self) -> None:
        finish_at = self.data_for_update.get("finish_at")

        if finish_at is None:
            return

        self.instance.finish_at = finish_at

    async def _update_tag_id(self) -> None:
        tag_id = self.data_for_update.get("tag_id")

        if tag_id is None:
            return

        tag = await Tag.get_object(tag_id)

        if tag is None:
            raise ErrorUpdateObject(f"Тэг с id={tag_id}, не найден")

        self.instance.tag_id = tag_id
