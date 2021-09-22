from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_superuser
from src.app.board.schemas import (
    GetCategory,
    CreateCategory
)
from src.app.board.service import category_s
from src.app.user.models import User

category_router = APIRouter()


@category_router.post('/', response_model=GetCategory)
async def create_category(
        schema: CreateCategory, user: User = Depends(get_superuser)
):
    return await category_s.create(schema)


@category_router.get('/', response_model=list[GetCategory])
async def get_categories():
    return await category_s.filter(parent_id__isnull=True)


@category_router.get('/{id}', response_model=GetCategory)
async def get_category(id: int):
    return await category_s.get(id=id)


@category_router.delete('/{id}')
async def delete_category(id: int, user: User = Depends(get_superuser)):
    return await category_s.delete(id=id)


@category_router.put('/{id}', response_model=GetCategory)
async def update_category(
        id: int, schema: CreateCategory, user: User = Depends(get_superuser)
):
    return await category_s.update(schema=schema, id=id)
