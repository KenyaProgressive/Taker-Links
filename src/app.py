import sys
from contextlib import asynccontextmanager
from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
from loguru import logger

from const import HOST, LOG_FORMAT, PORT
from db.session import _engine
from dependencies import LinksDataServiceDep
from dto.links_data import LinksDataDTO


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.remove()

    logger.add(
        sys.stderr,
        format=LOG_FORMAT,
        backtrace=True,
        diagnose=False,
    )

    yield

    await _engine.dispose()
    await logger.complete()


app: FastAPI = FastAPI(
    title="taker-links",
    lifespan=lifespan,
    description="Сокращатель ссылок в экосистеме Taker",
)


@app.get("/")
async def home():
    return "Weclome to Taker-Links!"


@app.get("/make_short")
async def make_short_link(service: LinksDataServiceDep, links_data: LinksDataDTO):
    try:
        res = await service.make_short_link(links_data)
        return JSONResponse(content={"short": res}, status_code=HTTPStatus.OK)
    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        return Response(
            content="Произошла ошибка. Попробуйте ещё раз.",
            status_code=HTTPStatus.BAD_REQUEST,
        )


@app.get("/{hash_token}")
async def make_redirect(service: LinksDataServiceDep, _hash: str):
    real_link = await service.get_real_link_by_hash(_hash)
    if real_link is not None:
        return RedirectResponse(real_link)
    else:
        return Response(content="Ресурс не найден", status_code=HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
