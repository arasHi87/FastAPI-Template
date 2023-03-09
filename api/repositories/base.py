from typing import Generic, Optional, Type, TypeVar

from models.base import Base
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model", bound=Base)
CreateModel = TypeVar("CreateModel", bound=BaseModel)
UpdateModel = TypeVar("UpdateModel", bound=BaseModel)

"""
Base CRUD class for all models
"""


class BaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model]):
        self.model = model

    async def create(self, db: AsyncSession, obj_in: CreateModel) -> Model:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: int) -> Optional[Model]:
        return await db.get(self.model, id)
