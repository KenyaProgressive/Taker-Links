from datetime import datetime
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.session import get_session
from fastapi import Depends
from repository.links_data_repository import LinksDataRepository
from dto.links_data import LinksDataDTO
from secrets import token_urlsafe
from const import BASE_LEN

class LinksDataService:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session
        self._repo = LinksDataRepository(session)
    
    async def _create_tables(self) -> None:
        await self._repo._create_tables()
        await self._session.commit()
    
    async def save_link(self, links_data: LinksDataDTO) -> str:
        try:
            _hash: str = self.make_hash(hash_len=links_data.custom_len)
            await self._repo.save_data(real_link=links_data.real_link, new_hash=)
            await self._session.commit()
            return _hash
        except Exception as e:
            await self._session.rollback()
            raise
    
    async def get_link_by_hash(self, hash: str) -> str | None:
        try:
            return await self._repo.get_data_by_hash(hash)
        except Exception as e:
            raise
    
    async def get_created_at_by_hash(self, hash: str)-> datetime | None:
        try:
            return await self._repo.get_created_at_by_hash(hash)
        except Exception as e:
            raise

    @staticmethod
    def make_hash(hash_len: int | None = BASE_LEN):
        if hash_len is None:
            hash_len = BASE_LEN
        return token_urlsafe(hash_len)





