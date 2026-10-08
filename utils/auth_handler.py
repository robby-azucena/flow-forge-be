from uuid import UUID

from fastapi import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.util.cython import uint
from sqlmodel import Session, select
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from config.database import db
from constants.response_message import FAILED_VALIDATE_CREDS, INVALID_CRED, USER_NOT_FOUND
from models.user import User
from utils.jwt_handler import decode_jwt
from utils.password_handler import verify_password


def get_user_by_user_id(session:Session, user_id:str):
    try:
        logger.info("Get user_id: " + user_id)
        return session.exec(select(User).where(User.id == user_id))
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=USER_NOT_FOUND
        )

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    cred_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=FAILED_VALIDATE_CREDS,
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = decode_jwt(token)
    if payload is None:
        raise cred_exception

    user_id = payload.get("sub")
    if not isinstance(user_id, str):
        raise cred_exception

    try:
        user_id = UUID(user_id)
    except ValueError:
        raise cred_exception

    try:
        with Session(db.get_engine()) as session:
            user = session.get(User, user_id)
            if user is None:
                raise cred_exception
            return user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
