from fastapi import APIRouter, Depends
from fastapi_user_limiter.limiter import rate_limiter
from fastapi_utils.cbv import cbv
from starlette.requests import Request

from config.database import db
from models.user import User
from schemas.create_user_schema import CreateUserSchema
from services.user import UserService
from utils import get_client_ip
from utils.custom_logging import log

router = APIRouter()
tag = "Users"

@cbv(router)
class UserController:
    user_service = UserService(db)

    @router.post("/create/",tags=[tag], dependencies=[Depends(rate_limiter(5,60, user=get_client_ip))])
    async def create_user(self, request:Request, user_form: CreateUserSchema, user:User):
        request.state.audit_event = "USER_CREATE"
        request.state.user = user.id

        user_id = user.id
        await log("user.info", method="POST", stage="REQUEST")

