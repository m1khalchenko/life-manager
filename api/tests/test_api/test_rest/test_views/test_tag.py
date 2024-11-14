import pytest
import pytest_asyncio
from rest.extensions import db
from rest.factories import TagFactory
from rest.models import Tag
from rest.schemas.tag import CreateTagSchema
from sqlalchemy import select


@pytest_asyncio.fixture
async def tag():
    data = CreateTagSchema(name="test tag")
    tag = await TagFactory(
        data_for_create=data.model_dump(),
    ).create()
    yield tag
    await Tag.delete_object(tag.id)


class TestTagViews:

    @pytest.mark.asyncio
    async def test_get_tags(self, app, tag: Tag):
        resp = await app.get("/tags")

        assert resp.status_code == 200
        assert resp

    @pytest.mark.asyncio
    async def test_get_tag(self, app, tag: Tag):
        resp = await app.get(f"/tag/{tag.id}")

        assert resp.status_code == 200
        assert resp.json()["name"] == tag.name

    @pytest.mark.asyncio
    async def test_delete_tag(self, app, tag: Tag):
        resp = await app.delete(f"/tag/{tag.id}")

        assert resp.status_code == 200

        tag = await db.first(select(Tag).where(Tag.id == tag.id))

        assert tag is None

    @pytest.mark.asyncio
    async def test_update_tag(self, app, tag: Tag):
        resp = await app.patch(
            f"/tag/{tag.id}",
            json={
                "name": "updated tag",
            },
        )

        assert resp.status_code == 200
        assert resp.json()["name"] == "updated tag"

    @pytest.mark.asyncio
    async def test_create_tag(self, app):
        resp = await app.post("/tags", json={"name": "new tag"})

        assert resp.status_code == 200
        assert resp.json()["name"] == "new tag"
