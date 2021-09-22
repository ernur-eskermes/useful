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
    parent_id: Optional[int] = 0

    class Config:
        orm_mode = True
        orig_model = Category


class GetCategory(CreateCategory):
    id: int
    children: list[CreateCategory]


class CreateToolkit(PydanticModel):
    name: str
    parent_id: Optional[int] = 0

    class Config:
        orm_mode = True
        orig_model = Toolkit


class GetToolkit(CreateToolkit):
    id: int


class CreateProject(PydanticModel):
    name: str
    description: str
    category_id: int
    toolkit_id: int

    # team: list[int]

    class Config:
        orm_mode = True
        orig_model = Project


class GetProject(CreateProject):
    id: int
    create_date: datetime
    category: GetCategory
    user_id: int


class CreateTask(PydanticModel):
    description: str
    start_date: datetime
    end_date: datetime
    project_id: int
    worker_id: Optional[int] = 0

    class Config:
        orm_mode = True
        orig_model = Task


class GetTask(CreateTask):
    id: int
    create_date: datetime


class CreateCommentTask(PydanticModel):
    message: str
    task_id: int

    class Config:
        orm_mode = True
        orig_model = CommentTask


class GetCommentTask(CreateCommentTask):
    id: int
    create_date: datetime
    user_id: int
