from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import BackgroundTasks
from tortoise.query_utils import Q

from src.app.user import schemas, service
from src.app.user.models import User
from src.config import settings
from .jwt import ALGORITHM
from .models import Verification
from .schemas import VerificationInDB
from .send_email import send_new_account_email

password_reset_jwt_subject = "preset"


async def registration_user(
        schema: schemas.UserCreateInRegistration,
        task: BackgroundTasks
) -> bool:
    """ Регистрация/верификация пользователя """
    if await User.filter(
            Q(username=schema.username) | Q(email=schema.email)
    ).exists():
        return True
    user = await service.user_s.create_user(schema)
    verify = await Verification.create(user_id=user.id)
    task.add_task(
        send_new_account_email,
        email_to=schema.email,
        username=schema.username,
        password=schema.password,
        uuid=verify.link
    )
    return False


async def verify_registration_user(uuid: VerificationInDB) -> bool:
    """ Подтверждение пользователя """
    verify = await Verification.get(link=uuid.link)
    if not verify:
        return False
    await User.filter(id=verify.user_id).update(is_active=True)
    await Verification.filter(link=uuid.link).delete()
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
