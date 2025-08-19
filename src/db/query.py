import aiosqlite
from logger import logger

DATABASE_NAME="links-data"


async def create_db_and_table() -> None:
    async with aiosqlite.connect(DATABASE_NAME) as conn:
        await create_table(conn)
        await conn.commit()


async def get_cursor(conn) -> aiosqlite.Cursor:
    return await conn.cursor()

async def create_table(conn) -> None:
    cursor = await get_cursor(conn)
    await cursor.execute(
        """CREATE TABLE IF NOT EXISTS tlink(id INTEGER PRIMARY KEY AUTOINCREMENT,
        real_link TEXT NOT NULL,
        hash TEXT NOT NULL,
        hash_link TEXT NOT NULL)"""
    )
    await conn.commit()

async def save_data(conn: aiosqlite.Connection) -> bool:
    cursor = await get_cursor(conn)
    try:
        await cursor.execute(
            """INSERT INTO tlink(id, real_link, hash, hash_link) VALUES(?, ?, ?, ?)""",
        )
        logger.info("'\033[94m'LINK GENERATE SUCESSFULLY --- DATA WAS SAVED'\033[0m'")
        await conn.commit()
        return True
    except aiosqlite.DatabaseError as e:
        logger.error(e)
        return False

async def get_real_link(conn: aiosqlite.Connection, hash_link: str):
    cursor = await get_cursor(conn)
    try:
        await cursor.execute("""SELECT real_link FROM tlink WHERE hash_link = ?""", hash_link)
        logger.info("REAL LINK WAS RETURNED SUCCESSFULLY")
    except aiosqlite.DatabaseError as e:
        logger.error(e)
