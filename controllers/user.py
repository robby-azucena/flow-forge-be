from fastapi import APIRouter
from fastapi_utils.cbv import cbv
router = APIRouter()

@cbv(router)
class UserController:
    user_service = 