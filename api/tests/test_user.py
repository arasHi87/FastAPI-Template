from app import APP
from fastapi import FastAPI
from tests import RequestBody, ResponseBody, assert_request

""" Test create user endpoint
@router post /user/
@status_code 201
@response_model schemas.User
@name user:create_user
"""


async def test_create_user_success(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="user:create_user"),
        body={"email": "test@gmail.com", "password": "test", "name": "test"},
    )
    resp = ResponseBody(
        status_code=201,
        body={
            "name": "test",
            "email": "test@gmail.com",
            "password": "7ec56ba8121cc89a1b3d84b4cfa0f2ed",
            "id": 2,
        },
    )
    await assert_request(app=APP, method="POST", req_body=req, resp_body=resp)


async def test_create_user_exists(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="user:create_user"),
        body={"name": "default", "email": "default@gmail.com", "password": "default"},
    )
    resp = ResponseBody(status_code=400, body={"detail": "User already exists"})
    await assert_request(app=APP, method="POST", req_body=req, resp_body=resp)


""" Test get user endpoint
@router get /user/
@status_code 200
@response_model schemas.UserWithoutPassword
@name user:get_user
"""


async def test_get_user_success(app: FastAPI):
    req = RequestBody(url=app.url_path_for(name="user:get_user", user_id=1), body={})
    resp = ResponseBody(
        status_code=200, body={"id": 1, "name": "default", "email": "default@gmail.com"}
    )
    await assert_request(app=APP, method="GET", req_body=req, resp_body=resp)


async def test_get_user_none_exists(app: FastAPI):
    req = RequestBody(url=app.url_path_for(name="user:get_user", user_id=100), body={})
    resp = ResponseBody(status_code=404, body={"detail": "User not found"})
    await assert_request(app=APP, method="GET", req_body=req, resp_body=resp)


""" Test update user endpoint
@router put /user/
@status_code 200
@response_model schemas.UserWithoutPassword
@name user:update_user
"""


async def test_update_user_success(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="user:update_user", user_id=1),
        body={
            "name": "test",
            "email": "test@gmail.com",
            "password": "default",
            "new_password": "test",
        },
    )
    resp = ResponseBody(
        status_code=200, body={"id": 1, "name": "test", "email": "test@gmail.com"}
    )
    await assert_request(app=APP, method="PUT", req_body=req, resp_body=resp)


async def test_update_user_none_exists(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="user:update_user", user_id=100),
        body={
            "name": "test",
            "email": "test@gmail.com",
            "password": "default",
            "new_password": "test",
        },
    )
    resp = ResponseBody(status_code=404, body={"detail": "User not found"})
    await assert_request(app=APP, method="PUT", req_body=req, resp_body=resp)


async def test_update_user_with_wrong_password(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="user:update_user", user_id=1),
        body={
            "name": "test",
            "email": "test@gmail.com",
            "password": "test",
            "new_password": "test",
        },
    )
    resp = ResponseBody(status_code=400, body={"detail": "Wrong password"})
    await assert_request(app=APP, method="PUT", req_body=req, resp_body=resp)


async def test_update_user_with_existing_email(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="user:update_user", user_id=1),
        body={
            "name": "meow",
            "email": "test@gmail.com",
            "password": "default",
            "new_password": "default",
        },
    )
    resp = ResponseBody(status_code=400, body={"detail": "Email already exists"})
    await test_create_user_success(app)
    await assert_request(app=APP, method="PUT", req_body=req, resp_body=resp)


""" Test delete user endpoint
@router delete /user/
@status_code 200
@response_model schemas.Msg
@name user:delete_user
"""


async def test_delete_user_success(app: FastAPI):
    req = RequestBody(url=app.url_path_for(name="user:delete_user", user_id=1), body={})
    resp = ResponseBody(status_code=200, body={"detail": "OK"})
    await assert_request(app=APP, method="DELETE", req_body=req, resp_body=resp)

    # make sure user is deleted
    await test_get_user_none_exists(app)


async def test_delete_user_none_exists(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="user:delete_user", user_id=100), body={}
    )
    resp = ResponseBody(status_code=404, body={"detail": "User not found"})
    await assert_request(app=APP, method="DELETE", req_body=req, resp_body=resp)
