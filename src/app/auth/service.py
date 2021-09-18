from datetime import timedelta, datetime
from typing import Optional

import jwt
from sqlalchemy.orm import Session

from src.app.user import crud, schemas
from src.config import settings
from .crud import auth_verify
from .jwt import ALGORITHM
from .schemas import VerificationInDB, VerificationCreate
from .send_email import send_new_account_email

password_reset_jwt_subject = "preset"


def registration_user(
        new_user: schemas.UserCreateInRegistration,
        db: Session
) -> bool:
    """ Регистрация/верификация пользователя """
    if crud.user.exists(db, username=new_user.username, email=new_user.email):
        return True
    user = crud.user.create(db, schema=new_user)
    verify = auth_verify.create(
        db,
        schema=VerificationCreate(user_id=user.id)
    )
    send_new_account_email(
        new_user.email,
        new_user.username,
        new_user.password,
        verify.link
    )
    return False


def verify_registration_user(uuid: VerificationInDB, db: Session) -> bool:
    """ Подтверждение пользователя """
    verify = auth_verify.get(db, link=uuid.link)
    if not verify:
        return False
    user = crud.user.get(db, id=verify.user_id)
    crud.user.update(
        db,
        obj=user,
        schema=schemas.UserUpdate(**{"is_active": "true"})
    )
    auth_verify.remove(db, link=uuid.link)
    return True


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": password_reset_jwt_subject,
         "email": email},
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except jwt.InvalidTokenError:
        return None
