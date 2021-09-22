from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_superuser
from src.app.blog.schemas import GetTag, CreateTag
from src.app.blog.service import tag_s
from src.app.user.models import User

tag_router = APIRouter()


@tag_router.post('/', response_model=GetTag)
async def create_tag(schema: CreateTag, user: User = Depends(get_superuser)):
    return await tag_s.create(schema)


@tag_router.get('/', response_model=list[GetTag])
async def get_tags():
    return await tag_s.all()


@tag_router.get('/{id}', response_model=GetTag)
async def get_tag(id: int):
    return await tag_s.get(id=id)


@tag_router.put('/{id}', response_model=GetTag)
async def update_tag(id: int, schema: CreateTag,
                     user: User = Depends(get_superuser)):
    return await tag_s.update(schema, id=id)


@tag_router.delete('/{id}', status_code=204)
async def delete_tag(id: int, user: User = Depends(get_superuser)):
    return await tag_s.delete(id=id)
