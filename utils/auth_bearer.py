from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from constants.response_message import (
    INVALID_AUTH_CODE,
    INVALID_AUTH_SCHEME,
    INVALID_TOKEN,
)
from utils.jwt_handler import decode_jwt, verify_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(
            request
        )

        if credentials is None:
            raise HTTPException(status_code=403, detail=INVALID_AUTH_CODE)

        if credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=403, detail=INVALID_AUTH_SCHEME)

        if not verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail=INVALID_TOKEN)

        payload = decode_jwt(credentials.credentials)

        if payload is None:
            raise HTTPException(status_code=403, detail=INVALID_TOKEN)

        request.state.user = payload["sub"]
        return credentials
