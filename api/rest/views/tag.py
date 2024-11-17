from typing import List

from fastapi import (
    APIRouter,
    HTTPException,
)
from rest.factories import TagFactory
from rest.models import Tag
from rest.schemas.tag import (
    CreateTagSchema,
    TagSchema,
    UpdateTagSchema,
)
from rest.utils.helpers.tag.tag_update import TagUpdate

router = APIRouter(tags=["tag"])


@router.post('/tags', response_model=TagSchema)
async def create_tag(data: CreateTagSchema) -> Tag:
    tag: Tag = await TagFactory(
        data_for_create=data.model_dump(),
    ).create()
    return tag


@router.get('/tags', response_model=List[TagSchema])
async def get_tags() -> List[Tag]:
    tags = await Tag.get_objects()
    return tags


@router.get('/tag/{tag_id}', response_model=TagSchema)
async def get_tag(tag_id: int) -> Tag:
    tag = await Tag.get_object(tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag


@router.delete('/tag/{tag_id}')
async def delete_tag(tag_id: int) -> None:
    await Tag.delete_object(tag_id)


@router.patch('/tag/{tag_id}', response_model=TagSchema)
async def update_tag(tag_id: int, data: UpdateTagSchema) -> Tag:
    timer = await Tag.get_object(tag_id)

    resp: Tag = await TagUpdate(
        data_for_update=data.model_dump(),
        instance=timer,
    ).update()

    return resp
