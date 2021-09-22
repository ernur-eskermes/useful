from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.app.auth.permissions import get_superuser
from src.app.blog.schemas import OutPost, CreatePost
from src.app.blog.service import post_s
from src.app.user.models import User

post_router = APIRouter()


@post_router.post('/', response_model=OutPost)
async def create_post(
        post: CreatePost,
        tags: list[int],
        user: User = Depends(get_superuser)
):
    return await post_s.create(post, tags, author_id=user.id)


@post_router.get('/', response_model=list[OutPost])
async def get_posts():
    return await post_s.filter(is_published=True)


@post_router.get('/filter', response_model=list[OutPost])
async def filter_post(
        category: str = '', tag: Optional[list[str]] = Query(None),
        skip: int = 0, limit: int = 10
):
    return await post_s.full_filter(
        category=category,
        tag=tag,
        skip=skip,
        limit=limit
    )


@post_router.get('/{id}', response_model=OutPost)
async def get_post(id: int):
    return await post_s.get(id=id)


@post_router.put('/{id}', response_model=OutPost)
async def update_post(
        id: int,
        schema: CreatePost,
        user: User = Depends(get_superuser)
):
    return await post_s.update(schema, id=id, author_id=user.id)


@post_router.delete('/{id}', status_code=204)
async def delete_post(id: int, user: User = Depends(get_superuser)):
    return await post_s.delete(id=id, author_id=user.id)
