from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_active_user
from src.app.user.models import User
from src.app.user.schemas import UserPublic

user_router = APIRouter()


@user_router.get('/me', response_model=UserPublic)
def user_me(current_user: User = Depends(get_active_user)):
    if current_user:
        return current_user
