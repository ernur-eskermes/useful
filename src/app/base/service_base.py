from typing import TypeVar, Optional

from fastapi import HTTPException
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

    async def create(self, schema: CreateSchemaType, **kwargs) -> GetSchemaType:
        obj = await self.model.create(
            **schema.dict(exclude_defaults=True),
            **kwargs
        )
        return await self.get_schema.from_tortoise_orm(obj)

    async def all(self) -> Optional[list[GetSchemaType]]:
        return await self.get_schema.from_queryset(self.model.all())

    async def update(self, schema, **kwargs) -> Optional[UpdateSchemaType]:
        await self.model.filter(**kwargs).update(
            **schema.dict(exclude_defaults=True)
        )
        return await self.get_schema.from_queryset_single(
            self.model.get(**kwargs)
        )

    async def delete(self, **kwargs):
        obj = await self.model.filter(**kwargs).delete()
        if not obj:
            raise HTTPException(
                status_code=404,
                detail='Object does not exist'
            )

    async def filter(self, **kwargs) -> Optional[list[GetSchemaType]]:
        return await self.get_schema.from_queryset(self.model.filter(**kwargs))

    async def get(self, **kwargs) -> Optional[GetSchemaType]:
        obj = self.model.get_or_none(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail='Object does not exist'
            )
        return await self.get_schema.from_queryset_single(obj)

    async def get_obj(self, **kwargs) -> Optional[ModelType]:
        return await self.model.get_or_none(**kwargs)
