from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from const import DATABASE_URL, ECHO
from typing import AsyncIterator

_engine: AsyncEngine = create_async_engine(url=DATABASE_URL, echo=ECHO)
_session_maker = async_sessionmaker(_engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with _session_maker() as session:
        yield session
