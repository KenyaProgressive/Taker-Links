import aiosqlite
import datetime
from logger import logger
from src.hasher import hasher

DATABASE_NAME="links-data"
HASH_RETENTION_TIME = 604800 # 7 days


async def create_db_and_table(conn: aiosqlite.Connection) -> None:
    try:
        await create_table(conn)
        await conn.commit()
    except Exception as e:
        logger.error(e)

async def get_cursor(conn) -> aiosqlite.Cursor:
    return await conn.cursor()

async def create_table(conn) -> None:
    cursor = await get_cursor(conn)
    await cursor.execute(
        """CREATE TABLE IF NOT EXISTS tlink(id INTEGER PRIMARY KEY AUTOINCREMENT,
        real_link TEXT NOT NULL,
        hash TEXT NOT NULL)"""
    )
    await conn.commit()
    await cursor.close()

async def save_data(conn: aiosqlite.Connection, real_link: str, new_hash: str) -> bool:
    cursor = await get_cursor(conn)
    try:
        await cursor.execute(
            """INSERT INTO tlink(real_link, hash) VALUES(?, ?)""",
            (real_link, new_hash))
        logger.info("'\033[94m'LINK GENERATE SUCESSFULLY --- DATA WAS SAVED'\033[0m'")
        await conn.commit()
        return True
    except aiosqlite.DatabaseError as e:
        logger.error(e)
        return False
    finally:
        await cursor.close()

async def get_real_link(conn: aiosqlite.Connection, hash_token: str):
    cursor = await get_cursor(conn)
    try:
        result = await cursor.execute("""SELECT real_link FROM tlink WHERE hash = ?""", (hash_token, ))
        return await result.fetchone()
    except aiosqlite.DatabaseError as e:
        logger.error(e)
    finally:
        await cursor.close()
    logger.info("REAL LINK WAS RETURNED SUCCESSFULLY")

async def check_time_existion(conn: aiosqlite.Connection, hash_token: str):
    cursor = await get_cursor(conn)
    now_time = datetime.datetime.now().timestamp()
    try:
        result = await cursor.execute("""SELECT created_at FROM tlink WHERE hash = ?""", (hash_token,))
        value = await result.fetchone()
        if now_time - value < 604800:
            return True
        return False
    except Exception as e:
        logger.error(e)
