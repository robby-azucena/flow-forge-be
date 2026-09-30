from fastapi import HTTPException
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from config.database import db
from constants.response_message import INVALID_CRED
from models.user import User
from utils.password_handler import verify_password


def get_user_by_email(session: Session, email_address: str):
    logger.info("Get user by email")
    try:
        logger.info(f"Email: {email_address}")
        return session.exec(select(User).where(User.email_address == email_address)).first()
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemyError:\n{e}")

        session.rollback()
        raise


def authenticate_user(email_address: str, password: str, session_id: str):
    logger.info("Authenticate user")
    with Session(db.get_engine()) as session, session.begin():
            logger.info("Session begin")

            user = get_user_by_email(session, email_address)

            if not user or not verify_password(password, user.hashed_password):
                logger.error(INVALID_CRED)
                raise HTTPException(status_code=401, detail=INVALID_CRED)

            user.session_id = session_id
            session.flush()
            session.refresh(user)
            return user.id
