SERVER_LINK = "http://localhost:8888"
DATABASE_NAME="links-data"
HASH_RETENTION_TIME = 604800 # 7 days
DATABASE_URL="sqlite+aiosqlite:///app.db"
ECHO=False
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
BASE_LEN = 6