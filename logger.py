from loguru import logger

LOG_STRING_FORMAT = "{time:DD.MM.YYYY-HH:mm:ss} --- {level} --- {message}"

logger.add(
    "logs/log.log",
     enqueue=True,
     format=LOG_STRING_FORMAT,
     retention="3 days"
)
