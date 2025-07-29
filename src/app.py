from fastapi import (
    FastAPI,
)
from src.hasher import hasher


tlinks = FastAPI(debug=True, title="Taker-Links")


@tlinks.get("/{real_link}")
async def index(real_link: str):
    new_hash: str = hasher()
