from config.database import DBConn
from repositories.user import UserRepositories


class UserService:
    def __init__(self, db:DBConn):
        self.db = db
        self.session = self.db.get_session()
        self.user_repo = UserRepositories()
