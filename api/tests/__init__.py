from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping, Optional

import schemas
from fastapi import FastAPI
from httpx import AsyncClient, Response
from starlette.datastructures import URLPath
from utils import create_access_token

DEFAULT_USER = schemas.UserWithoutPassword(
    id=1,
    name="default",
    email="default@gmail.com",
    password="default",
)


@dataclass
class RequestBody:
    url: URLPath
    body: Dict[str, Any]


@dataclass
class ResponseBody:
    status_code: int
    body: Dict[str, Any]


class AssertRequest:
    def __init__(self):
        claims = {**DEFAULT_USER.dict(), "exp": 123}
        self.header = {"Authorization": f"Bearer {create_access_token(claims=claims)}"}

    async def __call__(
        self,
        app: FastAPI,
        method: str,
        req_body: RequestBody,
        resp_body: ResponseBody,
        claims: Optional[Dict[str, Any]] = None,
        assert_func: Callable = None,
        data: Optional[Mapping[str, Any]] = None,
        header: Optional[Mapping[str, str]] = None,
        *args,
        **kwargs,
    ):
        if header is None:
            header = deepcopy(self.header)
            if claims is not None:
                header = {
                    "Authorization": f"Bearer {create_access_token(claims=claims)}"
                }

        async with AsyncClient(app=app, base_url="https://localhost") as ac:
            resp: Response = await ac.request(
                method=method,
                url=req_body.url,
                json=req_body.body,
                data=data,
                headers=header,
            )

            # If assert_func is not None, use assert_func to assert
            if assert_func is not None:
                assert_func(resp, resp_body, *args, **kwargs)
            else:
                assert resp.status_code == resp_body.status_code
                assert resp.json() == resp_body.body


assert_request = AssertRequest()
