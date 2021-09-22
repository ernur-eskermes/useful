from datetime import datetime

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from src.app.user.schemas import UserPublic
from .models import (
    BlogCategory,
    Tag,
    Post,
    Comment
)

CreateCategory = pydantic_model_creator(BlogCategory, exclude_readonly=True)
GetCategory = pydantic_model_creator(BlogCategory, exclude=('parent',))


class CategoryForPost(BaseModel):
    id: int
    name: str


CreateTag = pydantic_model_creator(Tag, exclude_readonly=True,
                                   exclude=('posts',))
GetTag = pydantic_model_creator(Tag, exclude=('posts',))

CreatePost = pydantic_model_creator(
    Post,
    exclude_readonly=True,
    exclude=('author_id',)
)

GetPost = pydantic_model_creator(
    Post,
    exclude=('is_published', 'category__children')
)


class OutPost(PydanticModel):
    id: int
    author: UserPublic
    tag: list[GetTag] = []
    category: CategoryForPost
    title: str
    mini_text: str
    text: str
    create_at: datetime
    publish_at: datetime
    image: str = None
    viewed: int
    description: str


CreateComment = pydantic_model_creator(
    Comment,
    exclude_readonly=True,
    exclude=('user_id', 'is_published', 'is_deleted', 'posts')
)

GetComment = pydantic_model_creator(
    Comment,
    exclude=('post', 'parent')
)


class UpdateComment(BaseModel):
    text: str


class OutComment(PydanticModel):
    id: int
    user: UserPublic
    post_id: int
    text: str
    create_at: datetime
    update_at: datetime


class CommentChildren(OutComment):
    children: list[OutComment]
