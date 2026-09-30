from cryptography.fernet import Fernet
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = []
    SECRET_KEY: str = "test-secret-key"
    DB_CONNECT_STRING: str = ""
    PASSWORD_ALGORITHM: str = "HS256"
    FERNET_KEY: bytes = Fernet.generate_key().decode().encode("utf-8")
    LOG_PATH: str=""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
