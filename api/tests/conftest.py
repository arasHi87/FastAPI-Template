import asyncio
from typing import Generator

import pytest
import schemas
from app import APP
from db import ASYNC_ENGINE as engine
from db import ASYNC_SESSION as session
from fastapi import FastAPI
from fastapi.testclient import TestClient
from models.base import Base
from models.user import User
from repositories.user import UserRepository
from tests import DEFAULT_USER

user_repo = UserRepository(User)


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(APP) as tc:
        yield tc


@pytest.fixture(scope="module")
def app() -> FastAPI:
    return APP


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse="True")
async def init_table(request):
    # Skip if test is marked as notableinit
    if "notableinit" in request.keywords:
        return

    # drop and create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # insert default data for user
    async with session() as conn:
        user = schemas.UserCreate(
            name=DEFAULT_USER.name,
            email=DEFAULT_USER.email,
            password=DEFAULT_USER.password,
        )
        await user_repo.create(conn, user)
