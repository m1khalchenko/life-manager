from rest.models import Tag
from rest.utils.helpers.base_update import BaseUpdate


class TagUpdate(BaseUpdate[Tag]):

    async def _update(self) -> None:
        await self._update_name()

    async def _update_name(self) -> None:
        name = self.data_for_update.get("name")

        if name is None or name == self.instance.name:
            return

        self.instance.name = name
