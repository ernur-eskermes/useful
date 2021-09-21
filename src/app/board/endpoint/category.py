from fastapi import APIRouter

from src.app.board.models import Category
from src.app.board.schemas import (
    GetCategory,
    CreateCategory
)
from src.app.board.service import category_s

category_router = APIRouter()


@category_router.post('/', response_model=GetCategory)
async def create_category(schema: CreateCategory):
    return await category_s.create(schema)


@category_router.get('/', response_model=list[GetCategory])
async def get_categories():
    return await GetCategory.from_queryset(Category.all())


@category_router.get('/{id}', response_model=GetCategory)
async def get_category(id: int):
    return await Category.get(id=id)


@category_router.delete('/{id}')
async def delete_category(id: int):
    return await Category.filter(id=id).delete()
