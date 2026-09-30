from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from constants.pathname import REFRESH_TOKEN_PATH
from constants.response_message import INVALID_ACCESS, INVALID_CRED
from schemas.auth_schema import RefreshTokenSchema, UserLoginSchema
from utils.auth_bearer import JWTBearer
from utils.auth_handler import authenticate_user
from utils.jwt_handler import refresh_jwt, sign_jwt

router = APIRouter()
tag = "Token"

@router.post("/", tags=[tag], dependencies=[])
async def user_login(
        request: Request, user_form: UserLoginSchema
):
    session_id = ""
    if "session_id" in request.state.session:
        session_id = request.state.session["session_id"]

    user = authenticate_user(email_address=user_form.email_address, password=user_form.password.get_secret_value(),
                             session_id=session_id)
    if user:
        return sign_jwt(str(user) , session_id)
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": INVALID_CRED})


@router.post(REFRESH_TOKEN_PATH, tags=[tag], dependencies=[  Depends(JWTBearer())])
async def refresh_token(
        request: Request, token: RefreshTokenSchema
):
    token = refresh_jwt(token.access_token)

    if token:
        return token
    else:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": INVALID_ACCESS})
