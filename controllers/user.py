from fastapi import APIRouter, Depends
from fastapi_user_limiter.limiter import rate_limiter
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from config.database import db
from schemas.create_user_schema import CreateUserSchema
from services.user import UserService
from utils.custom_logging import log
from utils.get_client_ip import get_client_ip

router = APIRouter()
tag = "Users"


@cbv(router)
class UserController:
    user_service = UserService(db)
    # Depends(rate_limiter(5, 60, user=get_client_ip))
    @router.post("/create/", tags=[tag], dependencies=[])
    async def create_user(self, request: Request, user_form: CreateUserSchema):
        request.state.audit_event = "USER_CREATE"

        await log("user.info", method="POST", stage="REQUEST", endpoint=request.url, payload=user_form.model_dump())

        new_user = self.user_service.create_user(user_form)

        await log("user.info", method="POST", stage="RESPONSE",
                  endpoint=request.url, status_code=HTTP_201_CREATED, response_data=new_user)
        return JSONResponse(new_user, status_code=HTTP_201_CREATED)
