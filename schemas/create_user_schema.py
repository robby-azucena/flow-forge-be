from pydantic import BaseModel, ConfigDict, EmailStr
from sqlmodel import Field


class CreateUserSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email_address: EmailStr = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)
