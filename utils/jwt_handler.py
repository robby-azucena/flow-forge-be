import time
from typing import TypedDict

import jwt
from loguru import logger

from config.settings import settings
from constants.auth import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES


class JWTPayload(TypedDict):
    sub: str
    session_id: str
    iat: float
    exp: float

def decode_jwt(token: str) -> dict[str,str] | None:
    try:
        logger.info("Decoding JWT...")
        logger.info(token)

        decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.PASSWORD_ALGORITHM],)
        logger.info(decode_token)

        exp = decode_token["exp"] >= time.time()
        logger.info(exp)
        return decode_token if exp else None
    except jwt.ExpiredSignatureError:
        logger.error("Expired Signature")
        return None
    except jwt.InvalidTokenError:
        logger.error("Invalid Token")

        return None

def verify_jwt(jwt_token: str) -> bool:
    logger.info("Verify JWT...")
    return decode_jwt(jwt_token) is not None

def token_response(access_token: str, refresh_token: str):
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

def sign_jwt(user_id: str, session_id: str) -> dict[str, str]:
    current_time = time.time()
    logger.info("Signing JWT...")

    payload: JWTPayload = {
        "sub": user_id,
        "session_id": session_id,
        "iat": current_time,
        "exp": current_time + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    }
    access = jwt.encode(dict(payload), settings.SECRET_KEY, algorithm=settings.PASSWORD_ALGORITHM)

    # Refresh
    payload["exp"] = current_time + (REFRESH_TOKEN_EXPIRE_MINUTES * 60)
    refresh = jwt.encode(dict(payload), settings.SECRET_KEY, algorithm=settings.PASSWORD_ALGORITHM)

    logger.info("User token created.")
    return token_response(access, refresh)

def refresh_jwt(token: str) -> dict[str, str] | None:
    logger.info("Refreshing token...")
    payload = decode_jwt(token)
    if payload is not None and "exp" in payload:
        current_time = time.time()

        # Access Generation
        payload["exp"] = current_time + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        access = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.PASSWORD_ALGORITHM)

        payload["exp"] = current_time + (REFRESH_TOKEN_EXPIRE_MINUTES * 60)
        refresh = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.PASSWORD_ALGORITHM)

        return token_response(access, refresh)

    return None
