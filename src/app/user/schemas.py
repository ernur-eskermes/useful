from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    first_name: Optional[str] = None


class UserBaseInDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


class UserCreate(UserBaseInDB):
    username: str
    email: str
    password: str
    first_name: str


class UserCreateInRegistration(BaseModel):
    username: str
    email: str
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


class UserPublic(UserBase):
    id: int

    class Config:
        orm_mode = True

