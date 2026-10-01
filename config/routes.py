from fastapi import APIRouter, FastAPI

from auth.auth import router as auth_router
from controllers.health_check import router as health_router
from controllers.user import router as user_router


def register_routes(app:FastAPI):
    api_router = APIRouter()

    api_router.include_router(router=health_router)
    api_router.include_router(router=auth_router , prefix="/token")
    api_router.include_router(router=user_router , prefix="/user")


    app.include_router(api_router)
