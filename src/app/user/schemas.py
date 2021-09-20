from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    first_name: Optional[str]
    avatar: Optional[str]


class UserBaseInDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


class UserCreate(UserBaseInDB):
    password: str


class UserCreateInRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str

    class Config:
        orm_mode = True


class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


class User(UserBaseInDB):
    pass


class UserInDB(UserBaseInDB):
    password: str


class SocialAccount(BaseModel):
    account_id: int
    account_url: str
    account_login: str
    account_name: str
    provider: str

    class Config:
        orm_mode = True


class UserPublic(UserBase):
    id: int
    social_account: Optional[list[SocialAccount]]

    class Config:
        orm_mode = True

