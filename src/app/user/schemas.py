from pydantic import EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from .models import User

UserCreate = pydantic_model_creator(
    User,
    name="UserCreate",
    exclude_readonly=True
)
UserUpdate = pydantic_model_creator(
    User,
    name="UserUpdate",
    exclude_readonly=True
)
UserGet = pydantic_model_creator(
    User,
    exclude=("password",),
    name="UserGet"
)


class UserCreateInRegistration(PydanticModel):
    username: str
    email: EmailStr
    password: str
    first_name: str


class UserPublic(PydanticModel):
    id: int
    first_name: str

# class UserBase(BaseModel):
#     username: Optional[str]
#     email: Optional[EmailStr]
#     is_active: Optional[bool]
#     is_superuser: Optional[bool]
#     first_name: Optional[str]
#     avatar: Optional[str]
#
#
# class UserBaseInDB(UserBase):
#     id: int = None
#
#     class Config:
#         orm_mode = True
#
#
# class UserCreate(UserBaseInDB):
#     password: str
#
#
#
#
# class UserUpdate(UserBaseInDB):
#     password: Optional[str] = None
#
#
# class UserInDB(UserBaseInDB):
#     password: str
#
#
# class SocialAccount(BaseModel):
#     account_id: int
#     account_url: str
#     account_login: str
#     account_name: str
#     provider: str
#
#     class Config:
#         orm_mode = True
#
#
# class UserPublic(UserBase):
#     id: int
#     social_account: Optional[list[SocialAccount]]
#
#     class Config:
#         orm_mode = True
