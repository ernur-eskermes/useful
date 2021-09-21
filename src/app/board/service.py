from src.app.base.service_base import BaseService
from . import schemas
from .models import (
    Category,
    Toolkit,
    Project,
    Task,
    CommentTask
)


class CategoryService(BaseService):
    model = Category
    create_schema = schemas.CreateCategory
    update_schema = schemas.CreateCategory
    get_schema = schemas.GetCategory


class ToolkitService(BaseService):
    model = Toolkit
    create_schema = schemas.CreateToolkit
    update_schema = schemas.CreateToolkit
    get_schema = schemas.GetToolkit


class ProjectService(BaseService):
    model = Project
    create_schema = schemas.CreateProject
    update_schema = schemas.CreateProject
    get_schema = schemas.GetProject


class TaskService(BaseService):
    model = Task
    create_schema = schemas.CreateTask
    update_schema = schemas.CreateTask
    get_schema = schemas.GetTask


class CommentTaskService(BaseService):
    model = CommentTask
    create_schema = schemas.CreateCommentTask
    update_schema = schemas.CreateCommentTask
    get_schema = schemas.GetCommentTask


category_s = CategoryService()
toolkit_s = ToolkitService()
project_s = ProjectService()
task_s = TaskService()
comment_task_s = CommentTaskService()
