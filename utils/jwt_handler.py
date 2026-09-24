import time
from typing import TypedDict, Dict

import jwt

from config.settings import settings
from constants.auth import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES


class JWTPayload(TypedDict):
    sub: str
    session_id: str
    iat: float
    exp: float

def decode_jwt(token: str) -> dict | None:
    try:
        decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.PASSWORD_ALGORITHM],)
        return decode_token if decode_token["exp"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def verify_jwt(jwt_token: str) -> bool:
    return decode_jwt(jwt_token) is not None

def token_response(access_token: str, refresh_token: str):
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

def sign_jwt(user_id: str, session_id: str) -> Dict[str, str]:
    current_time = time.time()

    payload: JWTPayload = {
        "sub": user_id,
        "session_id": session_id,
        "iat": current_time,
        "exp": current_time + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    }
    access = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.PASSWORD_ALGORITHM)

    # Refresh
    payload["exp"] = current_time + (REFRESH_TOKEN_EXPIRE_MINUTES * 60)
    refresh = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.PASSWORD_ALGORITHM)

    return token_response(access, refresh)

def refresh_jwt(token: str) -> Dict[str, str] | None:
    payload = decode_jwt(token)
    if "exp" in payload:
        current_time = time.time()

        # Access Generation
        payload["exp"] = current_time + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        access = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.PASSWORD_ALGORITHM)

        payload["exp"] = current_time + (REFRESH_TOKEN_EXPIRE_MINUTES * 60)
        refresh = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.PASSWORD_ALGORITHM)

        return token_response(access, refresh)

    return None