import os

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "8888"))
SERVER_LINK = os.getenv("PUBLIC_URL", f"http://{HOST}:{PORT}/")
DATABASE_NAME = "links-data"
HASH_RETENTION_TIME = 604800  # 7 days
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///app.db")
ECHO = False
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
BASE_LEN = 6
