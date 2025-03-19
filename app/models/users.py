from pydantic import EmailStr
import uuid

from fastapi_users import schemas
from app.models.base import ConfigMixin

#
# class UsersRegister(ConfigMixin):
#     login: str
#     email: EmailStr
#     password: str
#     referral_codes: str
#
#
# class UsersLogin(ConfigMixin):
#     login: str
#     email: EmailStr
#     password: str


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
