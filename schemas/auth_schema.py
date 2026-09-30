from pydantic import BaseModel, SecretStr, Field, EmailStr


class UserLoginSchema(BaseModel):
    email_address: EmailStr = Field(...)
    password: SecretStr = Field(...)

    class Config:
        json_schema_extra = {
            "example":{
                "email_address": "admin",
                "password": ""
            }
        }

class RefreshTokenSchema(BaseModel):
    refresh_token: str = Field(...)

    class Config:
         json_schema_extra = {
             "example":{
                 "refresh_token": "",
             }
         }

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
