from cryptography.fernet import Fernet
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MISTRAL_KEY: SecretStr = SecretStr("default-mistral-key")
    mistral_chat_model: str = "ministral-3b-2512"
    mistral_embedding_model: str = "mistral-embed-2312"
    chroma_persist_directory: str = "./chroma_db"
    ALLOWED_ORIGINS: list[str] = []
    SECRET_KEY: str = "test-secret-key"
    DB_CONNECT_STRING: str = ""
    PASSWORD_ALGORITHM: str = "HS256"
    FERNET_KEY: bytes = Fernet.generate_key().decode().encode("utf-8")
    REDIS_URL: str = ""
    LOG_PATH: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
