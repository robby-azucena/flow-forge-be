import uuid
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: uuid.UUID = Field(primary_key=True,default_factory=uuid.uuid4)
    email_address: EmailStr = Field(unique=True, index=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    hashed_password: str

    is_active: bool = Field(default=True)
    session_id: str = Field(default=None, nullable=True)

    password_change_on: datetime = Field(...)
    created_on: datetime = Field(default_factory=datetime.now)
    modified_on: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": datetime.now})

    password_history: list["PasswordHistory"] = Relationship(back_populates="user")


class PasswordHistory(SQLModel, table=True):
    __tablename__ = "password_history"
    id:uuid.UUID = Field(primary_key=True,default_factory=uuid.uuid4)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id", index=True)
    password_hash: str
    changed_on: datetime = Field(default_factory=datetime.now)
    user: Optional[User] = Relationship(back_populates="password_history")

class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profile"
    id:uuid.UUID = Field(primary_key=True,default_factory=uuid.uuid4)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id", index=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email_address: EmailStr = Field(...)
    is_active: bool = Field(default=True)