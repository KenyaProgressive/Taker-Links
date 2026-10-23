import asyncio

import aiosqlite
import uvicorn

from logger import logger
from src.app import tlinks
from src.db.query import DATABASE_NAME, create_db_and_table
from logger import logger_setup


def make_server(host: str, port: int) -> uvicorn.Server:
    logger_setup()
    conf = uvicorn.Config(tlinks, host=host, port=port, loop="asyncio")
    server = uvicorn.Server(conf)
    return server

async def main():
    server = make_server("localhost", 8888)
    await server.serve()
    logger.complete()

if __name__ == "__main__":

    asyncio.run(main())
