import asyncio

import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import (
    ASGITransport,
    AsyncClient,
)
from rest.app import create_app
from rest.extensions import config
from sqlalchemy import create_engine
from sqlalchemy_utils import (
    create_database,
    database_exists,
    drop_database,
)


@pytest_asyncio.fixture
async def app():
    _app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=_app), base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def recreate_db():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI_TEST_ALEMBIC)
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)

    alembic_cfg = Config('alembic.ini')
    command.upgrade(alembic_cfg, 'head')


def update_config_for_db():
    db_uri_for_test = config.SQLALCHEMY_DATABASE_URI_TEST
    config.SQLALCHEMY_DATABASE_URI = db_uri_for_test


def pytest_configure():
    update_config_for_db()
    recreate_db()
