from uuid import UUID

from pydantic import EmailStr

from config.response_schema import ResponseSchema
from models.user import User


class UserProfileResponseSchema(ResponseSchema):
    id: UUID
    email_address: EmailStr
    first_name: str
    last_name: str
    is_active: bool
