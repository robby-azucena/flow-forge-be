from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password:str, hashed_password:str ):
    print('Verifying password...')
    return pwd_context.verify(password, hashed_password)

def hash_password(password:str):
    print('Hashing password...')
    print("Password length:", len(password))
    print("Password bytes:", len(password.encode("utf-8")))

    return pwd_context.hash(password)
