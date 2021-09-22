from fastapi import APIRouter, Depends

from src.app.auth.permissions import get_superuser
from src.app.board.schemas import (
    GetToolkit,
    CreateToolkit
)
from src.app.board.service import toolkit_s
from src.app.user.models import User

toolkit_router = APIRouter()


@toolkit_router.post('/', response_model=GetToolkit)
async def create_toolkit(schema: CreateToolkit, user: User = Depends(get_superuser)):
    return await toolkit_s.create(schema)


@toolkit_router.get('/', response_model=list[GetToolkit])
async def get_toolkits():
    return await toolkit_s.filter(parent_id__isnull=True)


@toolkit_router.get('/{id}', response_model=GetToolkit)
async def get_toolkit(id: int):
    return await toolkit_s.get(id=id)


@toolkit_router.delete('/{id}', status_code=204)
async def delete_toolkit(id: int, user: User = Depends(get_superuser)):
    return await toolkit_s.delete(id=id)


@toolkit_router.put('/{id}', response_model=GetToolkit)
async def update_toolkit(
        id: int,
        schema: CreateToolkit,
        user: User = Depends(get_superuser)
):
    return await toolkit_s.update(schema=schema, id=id)
