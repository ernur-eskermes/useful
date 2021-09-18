from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_active_user
from . import schemas
from .models import User

user_router = APIRouter()


@user_router.get("/me", response_model=schemas.UserPublic)
def user_me(user: User = Depends(get_active_user)):
    return user
