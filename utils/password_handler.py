from passlib.context import CryptContext
from pydantic.v1 import EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password:str, hashed_password:str ):
    return pwd_context.verify(password, hashed_password)

def hash_password(password:EmailStr):
    return pwd_context.hash(password)