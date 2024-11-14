from datetime import datetime

import pytest
import pytest_asyncio
from rest.extensions import db
from rest.factories import TimerFactory
from rest.models import Timer
from rest.schemas.timer import CreateTimerSchema
from sqlalchemy import select


@pytest_asyncio.fixture
async def timer():
    data = CreateTimerSchema()
    timer = await TimerFactory(
        data_for_create=data.model_dump(),
    ).create()
    yield timer
    await Timer.delete_object(timer.id)


class TestTimerViews:

    @pytest.mark.asyncio
    async def test_get_timers(self, app, timer: Timer):
        resp = await app.get('/timers')

        assert resp.status_code == 200
        assert resp.json()[0]["start_at"]
        assert resp.json()[0]["result_time"]
        assert not resp.json()[0]["finish_at"]

    @pytest.mark.asyncio
    async def test_get_timer(self, app, timer: Timer):
        resp = await app.get(f'/timer/{timer.id}')

        assert resp.status_code == 200
        assert resp.json()["start_at"]
        assert resp.json()["result_time"]
        assert not resp.json()["finish_at"]

    @pytest.mark.asyncio
    async def test_delete_timer(self, app, timer: Timer):
        resp = await app.delete(f'/timer/{timer.id}')

        assert resp.status_code == 200

        timer = await db.first(select(Timer).where(Timer.id == timer.id))

        assert timer is None

    @pytest.mark.asyncio
    async def test_update_timer(self, app, timer: Timer):
        resp = await app.patch(
            f'/timer/{timer.id}',
            json={
                "finish_at": str(datetime.utcnow()),
            },
        )

        assert resp.status_code == 200
        assert resp.json()["start_at"]
        assert resp.json()["result_time"]
        assert resp.json()["finish_at"]

    @pytest.mark.asyncio
    async def test_create_timer(self, app):
        resp = await app.post("/timers", json={})

        assert resp.status_code == 200
        assert resp.json()["start_at"]
        assert resp.json()["result_time"]
