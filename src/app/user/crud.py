from typing import Optional

from sqlalchemy.orm import Session

from src.app.auth.security import verify_password, get_password_hash
from src.app.base.crud_base import CRUDBase
from .models import User
from .schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD for user"""

    def create(self, db: Session, schema: UserCreate, **kwargs) -> User:
        obj = User(
            username=schema.username,
            email=schema.email,
            password=get_password_hash(schema.password),
            first_name=schema.first_name
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
        if not verify_password(password, user.password):
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


user = CRUDUser(User)
