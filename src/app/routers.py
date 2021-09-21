from fastapi import APIRouter
from src.app.auth.api import auth_router
from src.app.board.endpoint.category import category_router
from src.app.board.endpoint.project import project_router
from src.app.board.endpoint.task import task_router
from src.app.board.endpoint.toolkit import toolkit_router
from src.app.user.api import user_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["login"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(category_router, prefix="/board/category", tags=["board"])
api_router.include_router(project_router, prefix="/board/project", tags=["board"])
api_router.include_router(toolkit_router, prefix="/board/toolkit", tags=["board"])
api_router.include_router(task_router, prefix="/board/task", tags=["board"])
