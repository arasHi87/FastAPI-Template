from dataclasses import dataclass
from typing import Any, Dict

from fastapi import FastAPI
from httpx import AsyncClient
from starlette.datastructures import URLPath


@dataclass
class RequestBody:
    url: URLPath
    body: Dict[str, Any]


@dataclass
class ResponseBody:
    status_code: int
    body: Dict[str, Any]


async def assert_request(
    app: FastAPI, method: str, req_body: RequestBody, resp_body: ResponseBody
):
    async with AsyncClient(app=app, base_url="https://localhost") as ac:
        resp = await ac.request(method=method, url=req_body.url, json=req_body.body)
        assert resp.status_code == resp_body.status_code
        assert resp.json() == resp_body.body
