from models.user import User
from schemas.user_profile_response_schema import UserProfileResponseSchema


def to_user_profile_mapper(user: User) -> UserProfileResponseSchema:
    profile = user

    return UserProfileResponseSchema(
        id=profile.id,
        email_address=profile.email_address,
        first_name=profile.first_name,
        last_name=profile.last_name,
        is_active=profile.is_active,
    )
