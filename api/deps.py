import schemas
from config import settings
from db import ASYNC_SESSION
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from loguru import logger
from pydantic import ValidationError
from repositories import user_repo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.APP_PREFIX}/auth")


async def get_db() -> AsyncSession:
    try:
        async with ASYNC_SESSION() as db:
            yield db
    except SQLAlchemyError as err:
        await db.rollback()
        logger.error(err)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> schemas.UserWithoutPassword:
    try:
        """payload @type: dict
        [int] @payload.id:    1
        [str] @payload.name:  m3ow87
        [str] @payload.email: arasi27676271@gmail.com
        [int] @payload.exp:   1620000000
        """
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ACCESS_TOKEN_ALGORITHM]
        )
        data = schemas.AuthTokenData(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # Check if user exists
    user = await user_repo.get(db, data.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
