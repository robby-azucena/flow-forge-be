import re

from pydantic import BaseModel, SecretStr, field_validator, model_validator

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64
PASSWORD_ALLOWED_CHARACTERS = "A-Za-z0-9!@#$%^&*()"


class ResetPasswordSchema(BaseModel):
    new_password: SecretStr
    confirm_password: SecretStr

    @staticmethod
    @field_validator("new_password", mode="before")
    def new_password_validator(v):
        if isinstance(v, SecretStr):
            password = v.get_secret_value()
        elif isinstance(v, str):
            password = v
        else:
            raise ValueError("Password must be a string")


        if len(password) < PASSWORD_MIN_LENGTH:
            raise ValueError("Password must be at least 8 characters long")
        if len(password) > PASSWORD_MAX_LENGTH:
            raise ValueError("Password must not exceed 64 characters")

        if not re.fullmatch(r"[" + PASSWORD_ALLOWED_CHARACTERS + "]+", password):
            raise ValueError("Password contains invalid characters")

        return SecretStr(password)

    @model_validator(mode="after")
    def check_is_password_match(self):
        if self.new_password.get_secret_value() != self.confirm_password.get_secret_value():
            raise ValueError("Password does not match")
        return self

