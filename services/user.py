import uuid

from fastapi.exceptions import HTTPException
from loguru import logger
from pydantic import ValidationError
from sqlmodel import Session
from starlette.status import HTTP_404_NOT_FOUND

from config.database import DBConn
from constants.response_message import USER_NOT_FOUND
from mappers.user_profile_mapper import to_user_profile_mapper
from models.user import User
from repositories.user import UserRepositories
from schemas.create_user_schema import CreateUserSchema
from utils.custom_logging import log


class UserService:
    def __init__(self, db: DBConn):
        self.db = db
        self.session = self.db.get_session()
        self.user_repo = UserRepositories()

    async def create_user(self, user: CreateUserSchema):

        await log("user.create", action="create_user", stage="START")
        with Session(self.db.get_engine(), expire_on_commit=False, ) as session, session.begin():
                try:
                    CreateUserSchema.model_validate(user)
                except ValidationError as e:
                    for err in e.errors():
                        field = err.get("loc", [None])[0]
                        context = err.get("ctx", {})
                        reason = context.get("reason", "Validation error occurred")
                        if field == "email":
                            raise ValueError(reason)

                new_user = self.user_repo.create_user(session, user)

                return new_user

    async def get_user_profile(self, user_id:uuid.UUID):
        logger.info("Get user profile service")
        await log("user.profile", action="get_user_profle", stage="START")

        if type(user_id) is not uuid.UUID:
            raise ValueError("Invalid user_id")

        user:User|None = self.user_repo.get_user_profile(self.session,user_id)

        user_profile = to_user_profile_mapper(user)



        return user_profile
