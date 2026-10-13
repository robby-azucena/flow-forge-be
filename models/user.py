import uuid
from datetime import UTC, datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


def utc_now():
    return datetime.now(UTC)


class User(SQLModel, table=True):
    __tablename__ = "user"  # type: ignore
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    email_address: EmailStr = Field(unique=True, index=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    hashed_password: str

    is_active: bool = Field(default=True)
    session_id: str = Field(default=None, nullable=True)

    password_change_on: datetime = Field(default_factory=utc_now)
    created_on: datetime = Field(default_factory=utc_now)
    modified_on: datetime | None = Field(
        default=None, sa_column_kwargs={"onupdate": utc_now}
    )

    password_history: list[PasswordHistory] = Relationship(back_populates="user")


class PasswordHistory(SQLModel, table=True):
    __tablename__ = "password_history"  # type: ignore
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", index=True)
    password_hash: str
    changed_on: datetime = Field(default_factory=utc_now)
    user: User | None = Relationship(back_populates="password_history")


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profile"  # type: ignore
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", index=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email_address: EmailStr = Field(...)
    is_active: bool = Field(default=True)
