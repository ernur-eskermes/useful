from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_active_user
from src.app.board.models import Project
from src.app.board.schemas import (
    GetProject,
    CreateProject
)
from src.app.board.service import project_s
from src.app.user.models import User

project_router = APIRouter()


@project_router.post('/', response_model=GetProject)
async def create_project(
        schema: CreateProject, user: User = Depends(get_active_user)
):
    return await project_s.create(schema, user_id=user.id)


@project_router.get('/', response_model=list[GetProject])
async def get_projects():
    return await project_s.all()


@project_router.get('/{id}', response_model=GetProject)
async def get_project(id: int):
    return await project_s.get(id=id)


@project_router.delete('/{id}', status_code=204)
async def delete_project(id: int, user: User = Depends(get_active_user)):
    return await project_s.delete(id=id, user_id=user.id)


@project_router.put('/{id}', response_model=GetProject)
async def update_project(
        id: int,
        schema: CreateProject,
        user: User = Depends(get_active_user)
):
    return await project_s.update(schema=schema, id=id, user_id=user.id)
