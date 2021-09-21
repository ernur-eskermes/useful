from fastapi import APIRouter

from src.app.board.models import Project
from src.app.board.schemas import (
    GetProject,
    CreateProject
)
from src.app.board.service import project_s

project_router = APIRouter()


@project_router.post('/', response_model=GetProject)
async def create_project(schema: CreateProject):
    return await project_s.create(schema)


@project_router.get('/', response_model=list[GetProject])
async def get_projects():
    return await GetProject.from_queryset(Project.all())


@project_router.get('/{id}', response_model=GetProject)
async def get_project(id: int):
    return await Project.get(id=id)


@project_router.delete('/{id}')
async def delete_project(id: int):
    return await Project.filter(id=id).delete()
