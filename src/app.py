from fastapi import (
    FastAPI,
)
from src.hasher import hasher
from src.db.query import save_data

tlinks = FastAPI(title="Taker-Links")


@tlinks.get("/{real_link}")
async def index(real_link: str):
    # new_hash: str = hasher()
    # await save_data(conn)
    return "Hello, World!"
