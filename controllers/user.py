from fastapi import APIRouter, Depends
from fastapi_user_limiter.limiter import rate_limiter
from fastapi_utils.cbv import cbv
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from config.database import db
from schemas.create_user_schema import CreateUserSchema
from services.user import UserService
from utils.auth_bearer import JWTBearer
from utils.auth_handler import get_current_user
from utils.custom_logging import log

router = APIRouter()
tag = "Users"


@cbv(router)
class UserController:
    user_service = UserService(db)

    # Depends(rate_limiter(5, 60, user=get_client_ip))
    @router.post("/create/", tags=[tag], dependencies=[])
    async def create_user(self, request: Request, user_form: CreateUserSchema):
        request.state.audit_event = "USER_CREATE"

        await log(
            "user.info",
            method="POST",
            stage="REQUEST",
            endpoint=request.url,
            payload=user_form.model_dump(),
        )

        if user_form.password != user_form.confirm_password:
            print("Passwords do not match")
            return JSONResponse(
                "Passwords do not match", status_code=HTTP_400_BAD_REQUEST
            )

        new_user = await self.user_service.create_user(user_form)

        await log(
            "user.info",
            method="POST",
            stage="RESPONSE",
            endpoint=request.url,
            status_code=HTTP_201_CREATED,
            response_data=new_user,
        )

        return JSONResponse(
            "New user created:" + new_user.email_address, status_code=HTTP_201_CREATED
        )

    @router.get("/profile/", tags=[tag], dependencies=[Depends(JWTBearer())])
    async def user_profile(self, request: Request, user=Depends(get_current_user)):
        user_id = user.id
        logger.info(f"Getting user profile using id: {user_id}")

        request.state.audit_event = "USER_PROFILE"

        await log(
            "user.profile",
            method="GET",
            stage="REQUEST",
            endpoint=request.url,
        )

        profile = await self.user_service.get_user_profile(user_id=user_id)

        return profile
