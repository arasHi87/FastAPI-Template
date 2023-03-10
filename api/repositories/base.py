from typing import Generic, Optional, Type, TypeVar

from models.base import Base
from pydantic import BaseModel
from sqlalchemy import and_, false
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

Model = TypeVar("Model", bound=Base)
CreateModel = TypeVar("CreateModel", bound=BaseModel)
UpdateModel = TypeVar("UpdateModel", bound=BaseModel)

"""
Base CRUD class for all models
"""


class BaseRepository(Generic[Model, CreateModel, UpdateModel]):
    def __init__(self, model: Type[Model]):
        self.model = model

    async def create(self, db: AsyncSession, obj_in: CreateModel) -> Model:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: int) -> Optional[Model]:
        result = await db.execute(
            select(self.model).where(
                and_(self.model.id == id, self.model.deleted == false())
            )
        )
        return result.scalars().first()

    async def update(
        self, db: AsyncSession, obj_in: UpdateModel, db_obj: Model
    ) -> Model:
        # Update data
        for field in obj_in.dict():
            setattr(db_obj, field, getattr(obj_in, field))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: Model):
        db_obj.deleted = True
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
