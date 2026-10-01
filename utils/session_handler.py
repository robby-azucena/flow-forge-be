import json
import uuid

import redis.asyncio as redis
from cryptography.fernet import Fernet
from fastapi import FastAPI
from fastapi.requests import Request
from loguru import logger

from config.settings import settings
from constants.auth import SESSION_EXPIRY
from constants.names import SESSION_ID

fernet = Fernet(settings.FERNET_KEY)


def session_handler(app: FastAPI):
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    logger.info("Redis Connected.")

    @app.middleware("http")
    async def redis_session_middleware(request: Request, call_next):
        logger.info("Access middleware")

        session_id = request.cookies.get(SESSION_ID)
        if not session_id:
            logger.info(f"Creating {SESSION_ID}")

            session_id = str(uuid.uuid4())
            request.state.session = {SESSION_ID: session_id}
        else:
            logger.info(f"Has {SESSION_ID}")

            session_data = await redis_client.get(session_id)

            try:
                request.state.session = json.loads(session_data) if session_data else {}
            except json.JSONDecodeError:
                logger.error("Session handler error")
                request.state.session = {}

            request.state.session[SESSION_ID] = session_id

        response = await call_next(request)

        await redis_client.setex(
            session_id, SESSION_EXPIRY, json.dumps(request.state.session)
        )

        response.set_cookie(
            session_id,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=SESSION_EXPIRY,
        )


        return response

def encrypt_session_data(data:dict) -> str:
    logger.info("Encrypt session")
    json_data = json.dumps(data)
    encrypted = fernet.encrypt(json_data.encode())
    return encrypted.decode()

def decrypt_session_data(token:str) -> dict:
    logger.info("Decrypt session")

    decrypted = fernet.decrypt(token.encode())
    return json.loads(decrypted)
