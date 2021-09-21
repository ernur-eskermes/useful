from datetime import datetime
from typing import Optional

from tortoise.contrib.pydantic import PydanticModel

from src.app.board.models import (
    Category,
    Project,
    Task,
    CommentTask,
    Toolkit
)


class CreateCategory(PydanticModel):
    name: str
    parent_id: Optional[int]


class GetCategory(CreateCategory):
    id: int

    class Config:
        orm_mode = True
        orig_model = Category


class CreateToolkit(PydanticModel):
    name: str
    parent_id: Optional[int] = 0


class GetToolkit(CreateToolkit):
    id: int

    class Config:
        orm_mode = True
        orig_model = Toolkit


class CreateProject(PydanticModel):
    name: str
    description: str
    user_id: int
    category_id: int
    toolkit_id: int
    # team: list[int]


class GetProject(CreateProject):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
        orig_model = Project


class CreateTask(PydanticModel):
    description: str
    start_date: datetime
    end_date: datetime
    project_id: int
    worker_id: int


class GetTask(CreateTask):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
        orig_model = Task


class CreateCommentTask(PydanticModel):
    message: str
    task_id: int
    user_id: int


class GetCommentTask(CreateCommentTask):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
        orig_model = CommentTask
