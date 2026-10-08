from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlmodel import Session, SQLModel

from config.settings import settings


class DBConn:
    def __init__(self, conn_str: str):
        self.conn_str = conn_str
        self.engine: Engine | None = None

    def get_engine(self) -> Engine:
        if self.engine is None:
            self.engine = create_engine(self.conn_str)

        return self.engine

    def get_session(self) -> Generator[Session]:
        with Session(self.get_engine()) as session:
            yield session

    def initialize(self) -> None:
        SQLModel.metadata.create_all(self.get_engine())


db = DBConn(settings.DB_CONNECT_STRING)
