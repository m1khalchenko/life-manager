import asyncio

from lazy_object_proxy.utils import await_
from rest.extensions import db

async def run() -> None:
    engine = db.create_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(db.metadata.drop_all)
        await conn.run_sync(db.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(run())
