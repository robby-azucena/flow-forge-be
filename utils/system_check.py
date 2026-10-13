from loguru import logger

from config.settings import settings


def system_check():
    logger.warning(f"Allowed origins: {len(settings.ALLOWED_ORIGINS ) != 0}")
    logger.warning(f"Database string: {settings.DB_CONNECT_STRING  != ""}")
    logger.warning(f"Log path: {settings.LOG_PATH}")
    logger.warning(f"Redis URL: {settings.REDIS_URL != ""}")
    logger.warning(f"Dev mode: {settings.DEV_MODE != ""}")
