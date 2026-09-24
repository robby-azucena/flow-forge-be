from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = []
    SECRET_KEY: str = "test-secret-key"
    DB_CONNECT_STRING: str = "sqlite:///test.db"
    PASSWORD_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()