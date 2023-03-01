from config import Config
from endpoints import health
from fastapi import APIRouter, Depends, FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from loguru import logger

APP = FastAPI(
    version=Config.APP_VERSION,
    title=Config.APP_TITLE,
    description=Config.APP_DESCRIPTION,
    openapi_url=Config.APP_OPENAPI_URL,
)

ROUTER = APIRouter()
ROUTER.include_router(health.router, prefix="/health", tags=["health"])


# Startup event
@APP.on_event("startup")
async def startup_event():
    logger.info("Processing startup initialization")


# Logs incoming request information
async def log_request(request: Request):
    logger.info(
        f"[{request.client.host}:{request.client.host}] {request.method} {request.url}"
    )
    logger.info(f"header: {request.headers}, body: ")
    logger.info(await request.body())


# Log response status code and body
@APP.middleware("http")
async def log_response(request: Request, call_next):
    response = await call_next(request)
    body = b""
    async for chunk in response.body_iterator:
        body += chunk

    logger.info(f"{response.status_code} {body}")

    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )


APP.include_router(
    ROUTER, prefix=Config.APP_PREFIX, dependencies=[Depends(log_request)]
)
