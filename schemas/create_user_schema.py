from pydantic import BaseModel, EmailStr, SecretStr, ConfigDict
from sqlmodel import Field


class CreateUserSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email_address: EmailStr = Field(...)
    password: SecretStr = Field(...)
    confirm_password: SecretStr = Field(...)