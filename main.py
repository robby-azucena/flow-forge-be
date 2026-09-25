from fastapi import FastAPI
from fastapi.params import Depends

from config.cors import setup_cors
from config.database import db
from config.routes import register_routes
from utils.auth_bearer import JWTBearer




app = FastAPI(dependencies=[
    Depends(db.get_session),
    Depends(JWTBearer())
],redirect_slashes=True)

setup_cors(app)
register_routes(app)


