from loguru import  logger
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_403_FORBIDDEN

from config.settings import settings


def setup_cors(app:FastAPI) -> None:
    logger.info("Setting up CORS...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



def origin_blocker(app:FastAPI):
    @app.middleware("http")
    async def block_unknown_origins(request: Request, call_next):
        origin = request.headers.get("origin")
        if origin and origin not in settings.ALLOWED_ORIGINS or origin is None:
            return JSONResponse({"detail": "Access denied"}, status_code=HTTP_403_FORBIDDEN)
        return await call_next(request)
