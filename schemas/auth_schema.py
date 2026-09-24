from pydantic import BaseModel, SecretStr, Field
from pydantic.v1 import EmailStr


class UserLoginSchema(BaseModel):
    email_address: EmailStr = Field(...)
    password: SecretStr = Field(...)

    class Config:
        json_schema_extra = {
            "example":{
                "username": "admin",
                "password": ""
            }
        }

class RefreshTokenSchema(BaseModel):
    access_token: str = Field(...)
#
# class UserSchema(BaseModel):
#     fullname: str = Field(...)
#     email: EmailStr = Field(...)
#     username: str = Field(...)
#
#     class Config:
#         json_schema_extra = {
#             "example":{
#                 "fullname": "",
#                 "email": "",
#                 "username": "",
#             }
#         }