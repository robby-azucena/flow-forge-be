from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.settings import settings


def setup_cors(app:FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )