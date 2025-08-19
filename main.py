import uvicorn
import asyncio
from src.app import tlinks
from logger import logger
from src.db.query import create_db_and_table

async def main():
    await create_db_and_table()
    conf = uvicorn.Config(tlinks, host='localhost', port=8888, loop="asyncio")
    server = uvicorn.Server(conf)
    await server.serve()
    logger.complete()


if __name__ == "__main__":
    asyncio.run(main())
