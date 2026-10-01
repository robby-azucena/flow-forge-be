from fastapi import FastAPI
from fastapi.params import Depends

from config.cors import setup_cors
from config.database import db
from config.routes import register_routes
from utils.session_handler import session_handler
from utils.system_check import system_check

system_check()

app = FastAPI(dependencies=[
    Depends(db.get_session),
], redirect_slashes=True)

setup_cors(app)
register_routes(app)
session_handler(app)
