from typing import TypeVar

from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import Model

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticModel)
GetSchemaType = TypeVar("GetSchemaType", bound=PydanticModel)


class BaseService:
    model: ModelType
    create_schema: CreateSchemaType
    update_schema: UpdateSchemaType
    get_schema: GetSchemaType

    async def create(self, schema: CreateSchemaType):
        obj = await self.model.create(**schema.dict(exclude_defaults=True))
        return await self.get_schema.from_tortoise_orm(obj)
