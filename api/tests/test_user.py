from app import APP
from fastapi import FastAPI
from httpx import AsyncClient

""" Test create user endpoint
@router post /user/
@status_code 201
@response_model schemas.User
@name user:create_user
"""


async def test_create_user_success(app: FastAPI):
    url = app.url_path_for(name="user:create_user")
    data = {"email": "test@gmail.com", "password": "test", "name": "test"}
    result = {
        "name": "test",
        "email": "test@gmail.com",
        "password": "7ec56ba8121cc89a1b3d84b4cfa0f2ed",
        "id": 2,
    }

    async with AsyncClient(app=APP, base_url="https://localhost") as ac:
        resp = await ac.post(url=url, json=data)
        assert resp.status_code == 201
        assert resp.json() == result


async def test_create_user_exists(app: FastAPI):
    url = app.url_path_for(name="user:create_user")
    data = {"name": "default", "email": "default@gmail.com", "password": "default"}
    result = {"detail": "User already exists"}

    async with AsyncClient(app=APP, base_url="https://localhost") as ac:
        resp = await ac.post(url=url, json=data)
        assert resp.status_code == 400
        assert resp.json() == result
