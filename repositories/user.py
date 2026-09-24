from uuid import UUID

from sqlmodel import Session, select

from models.user import UserProfile
from schemas.create_user_schema import CreateUserSchema


class UserRepositories:
    def create_user(self,session:Session, user: CreateUserSchema, user_id: UUID):
        profile_stm = select(UserProfile).where(UserProfile.email_address == user.email_address)
        existing_user = session.exec(profile_stm).first()

        if existing_user: