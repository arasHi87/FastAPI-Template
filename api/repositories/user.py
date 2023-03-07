import hashlib
from typing import Optional

from config import Config
from schemas.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    async def _get_hash_password(self, password: str) -> str:
        salt_pass = "".join([password, Config.PASSWORD_SALT])
        return hashlib.md5(salt_pass.encode()).hexdigest()

    async def create(self, db: AsyncSession, user: User) -> User:
        user.password = await self._get_hash_password(user.password)
        db_obj = self.model(**user.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(self.model).where(self.model.email == email))
        return result.scalars().first()
