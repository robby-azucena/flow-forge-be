from fastapi import FastAPI
from fastapi.params import Depends

from config.cors import setup_cors
from config.database import db
from config.settings import settings
from utils.auth_bearer import JWTBearer

print("ENV check:")
print("Allowed origins: ",settings.ALLOWED_ORIGINS)
print("DB connection string: ",settings.DB_CONNECT_STRING)
app = FastAPI(dependencies=[
    Depends(db.get_session()),
    Depends(JWTBearer())
],redirect_slashes=True)

setup_cors(app)


