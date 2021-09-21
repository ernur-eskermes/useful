from fastapi import APIRouter

from src.app.board.models import Toolkit
from src.app.board.schemas import (
    GetToolkit,
    CreateToolkit
)
from src.app.board.service import toolkit_s

toolkit_router = APIRouter()


@toolkit_router.post('/', response_model=GetToolkit)
async def create_toolkit(schema: CreateToolkit):
    return await toolkit_s.create(schema)


@toolkit_router.get('/', response_model=list[GetToolkit])
async def get_toolkits():
    return await GetToolkit.from_queryset(Toolkit.all())


@toolkit_router.get('/{id}', response_model=GetToolkit)
async def get_toolkit(id: int):
    return await Toolkit.get(id=id)


@toolkit_router.delete('/{id}')
async def delete_toolkit(id: int):
    return await Toolkit.filter(id=id).delete()
