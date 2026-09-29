from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from starlette.status import HTTP_400_BAD_REQUEST

from constants.response_message import (
    GENERIC_ERROR,
    USER_ALREADY_EXISTS,
    USER_CREATION_FAILED,
)
from models.user import User, UserProfile
from schemas.create_user_schema import CreateUserSchema
from schemas.reset_password_schema import ResetPasswordSchema
from utils.password_handler import hash_password


class UserRepositories:
    def create_user(self,session:Session, user: CreateUserSchema):
        profile_stm = select(UserProfile).where(UserProfile.email_address == user.email_address)
        existing_user = session.exec(profile_stm).first()

        if existing_user:
            session.rollback()
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=USER_ALREADY_EXISTS)

        try:
            hashed_password = hash_password(user.password)
            new_user = User(**user.model_dump(),
                            hashed_password=hashed_password)
            session.add(new_user)
            session.flush()

            new_profile = UserProfile(**user.model_dump())
            new_profile.user_id = new_user.id
            session.add(new_profile)
            session.flush()

            return new_user

        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=USER_CREATION_FAILED)
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=GENERIC_ERROR)

    def reset_password(self, session:Session, user:User, reset_password: ResetPasswordSchema):
        try:
            user.hashed_password = hash_password(reset_password.new_password.get_secret_value())
            user.password_changed_at = datetime.now(tz=timezone.utc)
            session.add(user)
            session.flush()
            return user
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=GENERIC_ERROR)
