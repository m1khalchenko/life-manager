from typing import List

from fastapi import APIRouter, HTTPException

from rest.factories import TagFactory
from rest.models import Tag
from rest.schemas import TagSchema
from rest.schemas.tag import CreateTagSchema

router = APIRouter(tags=["tag"])

@router.post('/tags')
async def create_tag(data: CreateTagSchema) -> TagSchema:
    tag = await TagFactory(
        data_for_create=data
    ).create()
    return tag

@router.get('/tags')
async def get_tags() -> List[TagSchema]:
    tags = await Tag.get_objects()
    return tags


@router.get('/tag/{tag_id}')
async def get_tag(tag_id: int) -> TagSchema:
    tag = await Tag.get_object(tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag


@router.delete('/tag/{tag_id}')
async def delete_tag(tag_id: int) -> None:
    await Tag.delete_object(tag_id)
