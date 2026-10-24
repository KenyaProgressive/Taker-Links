from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from const import DATABASE_URL, ECHO

_engine: AsyncEngine = create_async_engine(url=DATABASE_URL, echo=ECHO)
_session_maker = async_sessionmaker(_engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with _session_maker() as session:
        yield session
