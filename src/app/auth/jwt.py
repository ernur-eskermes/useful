from datetime import timedelta, datetime

import jwt

from src.config import settings

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(data: dict, expires_delta: timedelta = None) -> dict:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + \
                 timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": encoded_jwt, "token_type": "bearer"}
