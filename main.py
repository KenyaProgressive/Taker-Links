import uvicorn
import asyncio
from src.hasher import Hasher
from src.app import tlinks
from logger import logger

async def main():
    uvicorn.run(tlinks, host='localhost', port=8888)
    logger.complete()


if __name__ == "__main__":
    asyncio.run(main())
