from typing import Generator

from db import ASYNC_SESSION
from loguru import logger
from sqlalchemy.orm.session import Session


async def get_db() -> Generator:
    try:
        db: Session = ASYNC_SESSION()
        yield db
        db.commit()
    except Exception as err:
        db.rollback()
        logger.error(err)
    finally:
        db.close()
