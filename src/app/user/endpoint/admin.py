from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_superuser
from src.app.user.models import User
from src.app.user.schemas import (
    UserGet,
    UserCreate,
    UserUpdate,
    UserPublic
)
from src.app.user.service import user_s

admin_router = APIRouter()


@admin_router.get('/', response_model=list[UserPublic])
async def get_users(user: User = Depends(get_superuser)):
    return await user_s.all()


@admin_router.get('/{id}', response_model=UserGet)
async def get_user(id: int, user: User = Depends(get_superuser)):
    return await user_s.get(id=id)


@admin_router.post('/', response_model=UserGet)
async def create_user(
        schema: UserCreate,
        user: User = Depends(get_superuser)
):
    return await user_s.create_user(schema)


@admin_router.put('/{id}', response_model=UserGet)
async def update_user(
        id: int,
        schema: UserUpdate,
        user: User = Depends(get_superuser)
):
    return await user_s.update(schema, id=id)


@admin_router.delete('/{id}', status_code=204)
async def delete_user(id: int, user: User = Depends(get_superuser)):
    return await user_s.delete(id=id)
