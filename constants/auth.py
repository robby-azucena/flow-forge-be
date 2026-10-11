import time
from typing import Literal

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440
PASSWORD_EXPIRY_DAYS = 90
SESSION_EXPIRY = 60 * 60 * 24  # 1 day


def get_expiration_session(token_name: Literal["access", "refresh"]):
    current_time = time.time()

    if token_name == "access":
        return current_time + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    return current_time + (REFRESH_TOKEN_EXPIRE_MINUTES * 60)
