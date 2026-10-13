from loguru import logger
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def verify_password(password:str, hashed_password:str ):
    logger.info('Verifying password...')
    return password_hash.verify(password, hashed_password)

def hash_password(password:str):
    logger.info('Hashing password...')


    return password_hash.hash(password)
