from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from config.database import db

from sqlmodel import Session, select

from models.user import User
from utils.password_handler import verify_password



def get_user_by_email(session: Session, email_address: str):
    try:
        return session.exec(select(User).where(User.email_address == email_address)).first()
    except SQLAlchemyError:
        session.rollback()
        raise


def authenticate_user(email_address: str, password: str, session_id: str):
    with Session(db.get_engine()) as session:
        with session.begin():
            user = get_user_by_email(session, email_address)

            if not user or not verify_password(password, user.hashed_password):
                raise HTTPException(status_code=401, detail="Incorrect email or password")

            user.session_id = session_id
            session.flush()
            session.refresh(user)
            return user.id
