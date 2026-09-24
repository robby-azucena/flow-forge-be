from fastapi import APIRouter, FastAPI

from auth.auth import router as auth_router


def register_routes(app:FastAPI):
    api_router = APIRouter()

    api_router.include_router(router=auth_router , prefix="/token")

    app.include_router(api_router)
