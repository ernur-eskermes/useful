from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_superuser, get_active_user
from src.app.blog.schemas import (
    OutComment,
    CreateComment,
    CommentChildren,
    UpdateComment
)
from src.app.blog.service import comment_s
from src.app.user.models import User

comment_router = APIRouter()


@comment_router.post('/', response_model=OutComment)
async def create_comment(
        schema: CreateComment,
        user: User = Depends(get_active_user)
):
    return await comment_s.create(schema, user_id=user.id)


@comment_router.get('/', response_model=list[CommentChildren])
async def get_comments(user: User = Depends(get_superuser)):
    return await comment_s.all()


@comment_router.get('/filter', response_model=list[CommentChildren])
async def filter_comment(post_id: int, skip: int = 0, limit: int = 10):
    return await comment_s.filter(post_id=post_id, skip=skip, limit=limit)


@comment_router.get('/{id}', response_model=OutComment)
async def get_comment(id: int):
    return await comment_s.get(id=id)


@comment_router.put('/{id}', response_model=OutComment)
async def update_comment(
        id: int, schema: UpdateComment, user: User = Depends(get_active_user)
):
    return await comment_s.update(schema, id=id, user_id=user.id)


@comment_router.delete('/{id}', status_code=204)
async def delete_comment(id: int):
    return await comment_s.delete(id=id)
