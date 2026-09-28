import uuid

from config.database import DBConn
from repositories.user import UserRepositories
from schemas.create_user_schema import CreateUserSchema
from utils.custom_logging import log


class UserService:
    def __init__(self, db:DBConn):
        self.db = db
        self.session = self.db.get_session()
        self.user_repo = UserRepositories()


    async def create_user(self,user: CreateUserSchema, user_id:uuid.UUID):
        await log("user.create", action="create_user", stage="START", user_id=user_id)
