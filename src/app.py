import aiosqlite

from fastapi import (
    FastAPI,
)
from fastapi.responses import JSONResponse, RedirectResponse
from src.hasher import hasher
from src.db.query import check_time_existion, get_real_link, save_data, create_db_and_table, DATABASE_NAME
from src.validate import is_ip_address_valid, is_url_valid
from contextlib import asynccontextmanager
from logger import logger
from http import HTTPStatus

@asynccontextmanager
async def startup_and_shutdown(tlinks: FastAPI):
    tlinks.state.db_conn = await aiosqlite.connect(DATABASE_NAME)
    await create_db_and_table(tlinks.state.db_conn)
    yield
    await tlinks.state.db_conn.close()


tlinks = FastAPI(title="Taker-Links", lifespan=startup_and_shutdown)
SERVER_LINK = "http://localhost:8888"

@tlinks.get("/")
async def home():
    return "Weclome to Taker-Links!"

@tlinks.get("/convert")
async def convert_link(real_link: str):
    res = await get_real_link(tlinks.state.db_conn, real_link)
    if res != None:
        return JSONResponse(content={"SHORT_LINK": res}, status_code=HTTPStatus.OK)
    else:
        if is_ip_address_valid(real_link) or is_url_valid(real_link):
            try:
                new_hash_token = hasher()
                hash_link = SERVER_LINK + "/" + new_hash_token
                await save_data(tlinks.state.db_conn, real_link, new_hash_token)
                return JSONResponse(content={"SHORT_LINK": hash_link}, status_code=HTTPStatus.CREATED)
            except Exception as e:
                logger.error(e)
                return JSONResponse(content={"error": e}, status_code=HTTPStatus.BAD_REQUEST)

@tlinks.get("/{hash_token}")
async def make_redirect(hash_token: str):
    real_link = await get_real_link(tlinks.state.db_conn, hash_token)  # (link, )
    if real_link:
        return RedirectResponse(real_link[0])
    else:
        return JSONResponse(content={"error": "Not Found"}, status_code=HTTPStatus.NOT_FOUND)
