from schemas.article import Article, ArticleCreate, ArticleUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository


class ArticleRepository(BaseRepository[Article, ArticleCreate, ArticleUpdate]):
    async def create(
        self, db: AsyncSession, article: ArticleCreate, owner_id: int
    ) -> Article:
        db_obj = self.model(**article.dict(), owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
