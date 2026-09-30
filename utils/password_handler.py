from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def verify_password(password:str, hashed_password:str ):
    print('Verifying password...')
    return password_hash.verify(password, hashed_password)

def hash_password(password:str):
    print('Hashing password...')


    return password_hash.hash(password)
