from app import APP
from fastapi import FastAPI
from tests import DEFAULT_USER, RequestBody, ResponseBody, assert_request

""" Test create article endpoint
@router post /article/
@status_code 201
@response_model schemas.Article
@name article:create_article
@dependencies get_current_user, get_db
"""


async def test_create_article_success(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="article:create_article"),
        body={"title": "test", "description": "test", "body": "test"},
    )
    resp = ResponseBody(
        status_code=201,
        body={
            "title": "test",
            "description": "test",
            "body": "test",
            "id": 1,
            "owner_id": DEFAULT_USER.id,
        },
    )
    await assert_request(app=APP, method="POST", req_body=req, resp_body=resp)


async def test_create_article_auth_failed(app: FastAPI):
    req = RequestBody(
        url=app.url_path_for(name="article:create_article"),
        body={"title": "test", "description": "test", "body": "test"},
    )
    resp = ResponseBody(status_code=401, body={"detail": "Not authenticated"})
    await assert_request(
        app=APP, method="POST", req_body=req, resp_body=resp, header={}
    )
