from datetime import timedelta, datetime
from typing import Optional

import jwt
from sqlalchemy.orm import Session

from src.app.user import crud, schemas
from src.config import settings
from .crud import auth_verify
from .schemas import VerificationInDB
from .send_email import send_new_account_email

password_reset_jwt_subject = "preset"


def registration_user(new_user: schemas.UserCreateInRegistration, db: Session):
    if crud.user.exists(db, username=new_user.username, email=new_user.email):
        return True
    user = crud.user.create(db, obj_in=new_user)
    verify = auth_verify.create(db, user.id)
    send_new_account_email(
        new_user.email, new_user.username, new_user.password, verify.link)
    return False


def verify_registration_user(uuid: VerificationInDB, db: Session):
    verify = auth_verify.get(db, uuid.link)
    if not verify:
        return False
    user = crud.user.get(db, verify.user_id)
    crud.user.update(
        db,
        db_obj=user,
        obj_in=schemas.UserUpdate(**{"is_active": "true"})
    )
    auth_verify.remove(db, uuid.link)
    return True


def generate_password_reset_token(email):
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now - delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": password_reset_jwt_subject,
         "email": email},
        settings.SECRET_KEY,
        algorithm="HS@%^"
    )
    return encoded_jwt


def verify_password_reset_token(token) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        assert decoded_token["sub"] == password_reset_jwt_subject
        return decoded_token["email"]
    except jwt.InvalidTokenError:
        return None
