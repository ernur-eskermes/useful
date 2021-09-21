import jwt
from fastapi import Security, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN

from src.app.user.models import User
from src.config import settings
from .jwt import ALGORITHM
from .schemas import TokenPayload

password_reset_jwt_subject = "preset"
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


async def get_current_user(token: str = Security(reusable_oauth2)):
    """Получение текущего юзера"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = await User.get_or_none(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_active_user(current_user: User = Security(get_current_user)):
    """Проверка активный юзер или нет"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_superuser(current_user: User = Security(get_current_user)):
    """Проверка суперюзер или нет"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges"
        )
    return current_user
