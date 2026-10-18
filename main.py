from fastapi import FastAPI
from fastapi.params import Depends

from config.settings import settings
from config.cors import origin_blocker, setup_cors
from config.database import db
from config.routes import register_routes
from utils.session_handler import session_handler
from utils.system_check import system_check

system_check()

app = FastAPI(
    title="FlowForge",
    dependencies=[
        Depends(db.get_session),
    ],
    redirect_slashes=True,
    docs_url="/docs" if settings.DEV_MODE else None,
    redoc_url="/redocs" if settings.DEV_MODE else None,
    openapi_url="/openapi.json" if settings.DEV_MODE else None,
)

setup_cors(app)
register_routes(app)
# session_handler(app) # NOTE - Disabled for public portfolio. It should have dedicated redis server.
origin_blocker(app)
