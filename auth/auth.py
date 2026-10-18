from fastapi import APIRouter, Response
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from constants.names import SESSION_ID
from constants.pathname import REFRESH_TOKEN_PATH
from constants.response_message import INVALID_ACCESS, INVALID_CRED
from schemas.auth_schema import RefreshTokenSchema, UserLoginSchema
from utils.auth_handler import authenticate_user
from utils.jwt_handler import refresh_jwt, sign_jwt

router = APIRouter()
tag = "Token"


@router.post("/", tags=[tag], dependencies=[])
async def user_login(request: Request, response: Response, user_form: UserLoginSchema):
    logger.info("Getting token")
    session_id = ""

    session = getattr(request.state, "session", None) or {}
    if SESSION_ID in session:
        logger.info(f"Has {SESSION_ID}")

        session_id = request.state.session[SESSION_ID]
        logger.info("Getting token")

    user = authenticate_user(
        email_address=user_form.email_address,
        password=user_form.password.get_secret_value(),
        session_id=session_id,
    )
    if not user:
        logger.error(INVALID_CRED)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"detail": INVALID_CRED}
        )

    token = sign_jwt(str(user), session_id)
    logger.info("JWT Signed")

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite="lax",  # "none" only if truly cross-site
        max_age=15 * 60,  # match access token expiry
        path="/token",
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,  # match refresh token expiry
        path="/token",  # adjust to your real refresh route
    )

    return {"detail": "Logged in"}


@router.post(REFRESH_TOKEN_PATH, tags=[tag], dependencies=[])
async def refresh_token(
    request: Request, response: Response, token: RefreshTokenSchema
):
    new_token = refresh_jwt(token.refresh_token)

    if new_token:
        logger.info("New token success")

        response.set_cookie(
            key="access_token",
            value=new_token.access_token,
            httponly=True,
            secure=True,
            samesite="lax",  # "none" only if truly cross-site
            max_age=15 * 60,  # match access token expiry
            path="/token/refresh",
        )
        response.set_cookie(
            key="refresh_token",
            value=new_token.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,  # match refresh token expiry
            path="/token/refresh",  # adjust to your real refresh route
        )
        return new_token
    else:
        logger.error(INVALID_ACCESS)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"detail": INVALID_ACCESS}
        )
