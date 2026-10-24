from datetime import datetime
from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from db.session import _engine
from db.base import Base
from loguru import logger
from contextlib import asynccontextmanager
from db.links_data import LinksData
from datetime import timezone

class LinksDataRepository:

    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def _create_tables(self):
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created")

    async def save_data(self, real_link: str, new_hash: str) -> None:
        try:
            await self._session.execute(insert(LinksData).values(real_link=real_link, hash=new_hash))
        except Exception as e:
            logger.exception(f"Saving data doesn't ends successfully: {e}")
            raise
    
    async def get_data_by_hash(self, hash: str) -> str | None:
        try:
            return (await self._session.execute(select(LinksData.real_link).where(LinksData.hash == hash))).scalar_one_or_none()
        except Exception as e:
            logger.exception(f"Getting data doesn't ends successfully: {e}")
            raise
    
    async def get_created_at_by_hash(self, hash: str) -> datetime | None:
        try:
            return (await self._session.execute(select(LinksData.created_at).where(LinksData.hash == hash))).scalar_one_or_none()
        except Exception as e:
            logger.exception(f"Getting data doesn't ends successfully: {e}")
            raise


        