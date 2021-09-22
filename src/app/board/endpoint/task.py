from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_active_user
from src.app.board.schemas import (
    GetTask,
    CreateTask,
    GetCommentTask,
    CreateCommentTask
)
from src.app.board.service import task_s, comment_task_s
from src.app.user.models import User

task_router = APIRouter()


@task_router.post('/', response_model=GetTask)
async def create_task(schema: CreateTask):
    return await task_s.create(schema)


@task_router.get('/', response_model=list[GetTask])
async def get_tasks():
    return await task_s.all()


@task_router.get('/{id}', response_model=GetTask)
async def get_task(id: int):
    return await task_s.get(id=id)


@task_router.delete('/{id}')
async def delete_task(id: int):
    return await task_s.delete(id=id)


@task_router.put('/{id}', response_model=GetTask)
async def update_task(id: int, schema: CreateTask):
    return await task_s.update(schema=schema, id=id)


@task_router.post('/comment', response_model=GetCommentTask)
async def create_task_comment(
        schema: CreateCommentTask,
        user: User = Depends(get_active_user)
):
    return await comment_task_s.create(schema, user_id=user.id)


@task_router.get('/comment', response_model=list[GetCommentTask])
async def get_task_comments():
    return await comment_task_s.all()


@task_router.get('/comment/{id}', response_model=GetCommentTask)
async def get_task_comment(id: int):
    return await comment_task_s.get(id=id)


@task_router.delete('/comment/{id}')
async def delete_task_comment(id: int, user: User = Depends(get_active_user)):
    return await comment_task_s.delete(id=id, user_id=user.id)


@task_router.put('/{id}', response_model=GetCommentTask)
async def update_project(
        id: int,
        schema: CreateCommentTask,
        user: User = Depends(get_active_user)
):
    return await comment_task_s.update(schema=schema, id=id, user_id=user.id)
