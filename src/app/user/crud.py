from typing import Optional

from sqlalchemy.orm import Session

from src.app.auth.security import verify_password, get_password_hash
from src.app.base.crud_base import CRUDBase
from .models import User, SocialAccount
from . import schemas


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    """CRUD for user"""

    def create(
            self, db: Session, schema: schemas.UserCreate, **kwargs
    ) -> User:
        obj = User(
            **schema.dict(exclude={'password'}),
            password=get_password_hash(schema.password),
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def create_superuser(
            self, db: Session, schema: schemas.UserCreate
    ) -> User:
        obj = User(
            username=schema.username,
            email=schema.email,
            password=get_password_hash(schema.password),
            first_name=schema.first_name,
            is_active=schema.is_active,
            is_superuser=schema.is_superuser,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def authenticate(
            self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        obj = self.get(db, username=username)
        if not obj:
            return None
        if not verify_password(password, obj.password):
            return None
        return obj

    def is_active(self, obj: User) -> bool:
        return obj.is_active

    def is_superuser(self, obj: User) -> bool:
        return obj.is_superuser

    def change_password(self, db: Session, obj: User, new_password: str) -> None:
        hashed_password = get_password_hash(new_password)
        obj.password = hashed_password
        db.add(obj)
        db.commit()


class CRUDSocialAccount(
    CRUDBase[SocialAccount, schemas.SocialAccount, schemas.SocialAccount]
):
    """CRUD for Social Account"""
    pass


user = CRUDUser(User)
social_account = CRUDSocialAccount(SocialAccount)
