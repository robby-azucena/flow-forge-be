from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from config.settings import settings


class DBConn:
    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.engine = None

    def get_session(self):
        with Session(self.get_engine()) as session:
            yield session

    def initialize(self):
        SQLModel.metadata.create_all(self.get_engine())

    def _setup_engine(self):
        self.engine = create_engine(self.conn_str)

    def get_engine(self):
        if not self.engine:
            self._setup_engine()
        return self.engine

db = DBConn(settings.DB_CONNECT_STRING)