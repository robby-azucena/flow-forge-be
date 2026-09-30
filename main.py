from fastapi import FastAPI
from fastapi.params import Depends
from loguru import logger

from config.cors import setup_cors
from config.database import db
from config.routes import register_routes
from config.settings import settings
from utils.session_handler import session_handler

app = FastAPI(dependencies=[
    Depends(db.get_session),
], redirect_slashes=True)

setup_cors(app)
register_routes(app)
logger.warning(f"Allowed origins: {len(settings.ALLOWED_ORIGINS ) != 0}")
logger.warning(f"Database string: {settings.DB_CONNECT_STRING  != ""}")
logger.warning(f"Log path: {settings.LOG_PATH}")
session_handler(app)
