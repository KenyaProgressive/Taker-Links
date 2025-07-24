import aiosqlite

DATABASE_NAME="tlinks-db"

async def make_connection() -> aiosqlite.Connection:
    return await aiosqlite.connect(DATABASE_NAME)

async def get_cursor(conn: aiosqlite.Connection) -> aiosqlite.Cursor:
    return await conn.cursor()

async def create_table(conn: aiosqlite.Connection) -> None:
    cursor = await get_cursor(conn)
    await cursor.execute(
        """CREATE TABLE IF NOT EXISTS links-data (id INTEGER PRIMARY KEY AUTOINCREMENT,
        old_link TEXT NOT NULL,
        new_link TEXT NOT NULL)"""
    )
    await conn.commit()
