from db import ASYNC_SESSION
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncSession:
    try:
        async with ASYNC_SESSION() as db:
            yield db
    except SQLAlchemyError as err:
        await db.rollback()
        logger.error(err)
