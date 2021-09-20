from typing import TypeVar, Generic, Type, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def exists(self, db: Session, **kwargs) -> bool:
        return db.query(
            db.query(self.model.id).filter_by(**kwargs).exists()
        ).scalar()

    def get_object_or_404(self, db: Session, id: int) -> Optional[ModelType]:
        pass

    def get(self, db: Session, **kwargs) -> Optional[ModelType]:
        return db.query(self.model).filter_by(**kwargs).first()

    def filter(self, db: Session, **kwargs) -> list[ModelType]:
        return db.query(self.model).filter_by(**kwargs)

    def all(self, db: Session, skip=0, limit=100) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(
            self, db: Session, schema: CreateSchemaType, **kwargs
    ) -> ModelType:
        obj = self.model(**schema.dict(exclude={'avatar_url'}), **kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(
            self, db: Session, obj: ModelType, schema: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(obj)
        update_data = schema.dict(skip_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj, field, update_data[field])
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, **kwargs) -> ModelType:
        obj = self.get(db, **kwargs)
        db.delete(obj)
        db.commit()
        return obj
