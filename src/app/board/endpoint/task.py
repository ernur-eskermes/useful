from fastapi import APIRouter

from src.app.board.models import Task, CommentTask
from src.app.board.schemas import (
    GetTask,
    CreateTask,
    GetCommentTask,
    CreateCommentTask
)
from src.app.board.service import task_s, comment_task_s

task_router = APIRouter()


@task_router.post('/', response_model=GetTask)
async def create_task(schema: CreateTask):
    return await task_s.create(schema)


@task_router.get('/', response_model=list[GetTask])
async def get_tasks():
    return await GetTask.from_queryset(Task.all())


@task_router.get('/{id}', response_model=GetTask)
async def get_task(id: int):
    return await Task.get(id=id)


@task_router.delete('/{id}')
async def delete_task(id: int):
    return await Task.filter(id=id).delete()


@task_router.post('/comment', response_model=GetCommentTask)
async def create_task_comment(schema: CreateCommentTask):
    return await comment_task_s.create(schema)


@task_router.get('/comment', response_model=list[GetCommentTask])
async def get_task_comments():
    return await GetCommentTask.from_queryset(CommentTask.all())


@task_router.get('/comment/{id}', response_model=GetCommentTask)
async def get_task_comment(id: int):
    return await CommentTask.get(id=id)


@task_router.delete('/comment/{id}')
async def delete_task_comment(id: int):
    return await CommentTask.filter(id=id).delete()
