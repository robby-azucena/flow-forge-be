from config.database import DBConn


class UserService:
    def __init__(self, db:DBConn):
        self.db = db
        self.session = self.db.get_session()
        self.user_repo = 