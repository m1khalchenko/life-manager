#!/usr/bin/env python3
from alembic import command
from config import alembic_cfg
from rest.extensions import config
from sqlalchemy import create_engine
from sqlalchemy_utils import (
    create_database,
    database_exists,
    drop_database,
)


def run() -> None:
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI_ALEMBIC)
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)

    command.upgrade(alembic_cfg, 'head')


if __name__ == "__main__":
    run()
