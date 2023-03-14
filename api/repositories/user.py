import hashlib
from typing import Optional

from config import Config
from fastapi import HTTPException, status
from schemas.user import User, UserCreate, UserUpdate
from sqlalchemy import false
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def _get_hash_password(self, password: str) -> str:
        salt_pass = "".join([password, Config.SECRET_KEY])
        return hashlib.sha256(salt_pass.encode()).hexdigest()

    async def create(self, db: AsyncSession, user: UserCreate) -> User:
        user.password = self._get_hash_password(user.password)
        db_obj = self.model(**user.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(
            select(self.model).where(
                self.model.email == email and self.model.deleted == false()
            )
        )
        return result.scalars().first()

    async def update(self, db: AsyncSession, user: UserUpdate, db_obj: User) -> User:
        # Check password
        user.password = self._get_hash_password(user.password)
        if not user.password == db_obj.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password"
            )

        # Update data
        user.password = self._get_hash_password(user.new_password)
        for field in user.dict():
            setattr(db_obj, field, getattr(user, field))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, email: str, password: str
    ) -> Optional[User]:
        # Check if user exists
        user = await self.get_by_email(db, email)
        if not user:
            return None
        # Check if password is correct
        password = self._get_hash_password(password)
        if password != user.password:
            return None
        return user
