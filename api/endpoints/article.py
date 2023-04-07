import schemas
from deps import get_current_user, get_db
from fastapi import APIRouter, Depends, status
from models.article import Article
from repositories import article_repo
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

CREATE_ARTICLE = {
    201: {
        "description": "Article created successfully",
        "content": {"json": {"detail": "OK"}},
    },
    500: {
        "description": "Internal server error",
        "content": {"json": {"detail": "Internal server error"}},
    },
}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_ARTICLE,
    response_model=schemas.Article,
    name="article:create_article",
)
async def create_article(
    payload: schemas.ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    article: Article = await article_repo.create(db, payload, owner_id=current_user.id)
    return article
