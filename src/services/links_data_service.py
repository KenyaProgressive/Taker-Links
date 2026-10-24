import ipaddress
from datetime import datetime
from secrets import token_urlsafe

from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio.session import AsyncSession

from const import BASE_LEN, SERVER_LINK
from db.session import get_session
from dto.links_data import LinksDataDTO
from repository.links_data_repository import LinksDataRepository


class LinksDataService:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session
        self._repo = LinksDataRepository(session)
        self._server_url = SERVER_LINK

    async def _create_tables(self) -> None:
        await self._repo._create_tables()
        await self._session.commit()

    async def _save_link_and_get_hash(self, links_data: LinksDataDTO) -> str:
        try:
            _hash: str = self._make_hash(hash_len=links_data.custom_len)
            await self._repo.save_data(
                real_link=links_data.get_str_link(), new_hash=_hash
            )
            return _hash
        except Exception as e:
            await self._session.rollback()
            raise

    async def make_short_link(self, links_data: LinksDataDTO) -> str:
        try:

            exist_hash: str | None = await self._repo.get_hash_by_link(
                links_data.get_str_link()
            )
            if exist_hash:
                return f"{self._server_url}{exist_hash}"

            _hash = await self._save_link_and_get_hash(links_data)
            return f"{self._server_url}{_hash}"

        except Exception as e:
            raise

    async def get_hash_by_real_link(self, real_link: str) -> str | None:
        try:
            return await self._repo.get_hash_by_link(real_link)
        except Exception as e:
            raise

    async def get_real_link_by_hash(self, hash: str) -> str | None:
        try:
            return await self._repo.get_link_by_hash(hash)
        except Exception as e:
            raise

    async def get_created_at_by_hash(self, hash: str) -> datetime | None:
        try:
            return await self._repo.get_created_at_by_hash(hash)
        except Exception as e:
            raise

    @staticmethod
    def _make_hash(hash_len: int | None = BASE_LEN):
        if hash_len is None or hash_len < 1:
            hash_len = BASE_LEN
        return token_urlsafe(hash_len)
