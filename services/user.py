from pydantic import ValidationError
from sqlmodel import Session

from config.database import DBConn
from repositories.user import UserRepositories
from schemas.create_user_schema import CreateUserSchema
from utils.custom_logging import log


class UserService:
    def __init__(self, db: DBConn):
        self.db = db
        self.user_repo = UserRepositories()

    async def create_user(self, user: CreateUserSchema):

        await log("user.create", action="create_user", stage="START")
        with Session(self.db.get_engine(), expire_on_commit=False, ) as session:
            with session.begin():
                try:
                    CreateUserSchema.model_validate(user)
                except ValidationError as e:
                    for err in e.error():
                        if err["loc"][0] == "email":
                            raise ValueError(err["ctx"]["reason"])

                new_user = self.user_repo.create_user(session, user)

                return new_user
