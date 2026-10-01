from fastapi import APIRouter, Depends
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from constants.names import SESSION_ID
from constants.pathname import REFRESH_TOKEN_PATH
from constants.response_message import INVALID_ACCESS, INVALID_CRED
from schemas.auth_schema import RefreshTokenSchema, UserLoginSchema
from utils.auth_bearer import JWTBearer
from utils.auth_handler import authenticate_user
from utils.jwt_handler import refresh_jwt, sign_jwt

router = APIRouter()
tag = "Token"


@router.post("/", tags=[tag], dependencies=[])
async def user_login(request: Request, user_form: UserLoginSchema):
    logger.info("Getting token")
    session_id = ""
    if SESSION_ID in request.state.session:
        logger.info(f"Has {SESSION_ID}")

        session_id = request.state.session[SESSION_ID]

    user = authenticate_user(
        email_address=user_form.email_address,
        password=user_form.password.get_secret_value(),
        session_id=session_id,
    )
    if user:
        logger.info("Has user")

        return sign_jwt(str(user), session_id)
    logger.error(INVALID_CRED)
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"detail": INVALID_CRED}
    )


@router.post(REFRESH_TOKEN_PATH, tags=[tag], dependencies=[])
async def refresh_token(request: Request, token: RefreshTokenSchema):
    new_token = refresh_jwt(token.refresh_token)

    if new_token:
        logger.info("New token success")

        return new_token
    else:
        logger.error(INVALID_ACCESS)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"detail": INVALID_ACCESS}
        )
