from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import _engine
from db.base import Base
from loguru import logger
from contextlib import asynccontextmanager
from db.links_data import LinksData

class LinksDataRepository:

    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def _create_db(self):
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created")

    async def save_data(self, real_link: str, new_hash: str) -> None:
        try:
            link: LinksData = LinksData(real_link=real_link, hash=new_hash)
            self._session.add(link)
            await self._session.commit()
        except Exception as e:
            logger.error(f"Saving data doesn't ends: {e}")
            await self._session.rollback()
            raise
    
    async def get_data(self, hash: str) -> str:
        ...
        