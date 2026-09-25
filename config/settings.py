from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = []
    SECRET_KEY: str = "test-secret-key"
    DB_CONNECT_STRING: str = "sqlite:///test.db"
    PASSWORD_ALGORITHM: str = "HS256"
    LOG_PATH: str="./logs/"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

print("Allowed: ",settings.ALLOWED_ORIGINS is not None)
print("DB connection: ",settings.DB_CONNECT_STRING is not None)
print("Log path: ",settings.LOG_PATH is not None)