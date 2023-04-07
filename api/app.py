from config import settings
from endpoints import article, auth, health, user
from fastapi import APIRouter, Depends, FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
from loguru import logger

APP = FastAPI(
    version=settings.APP_VERSION,
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    openapi_url=settings.APP_OPENAPI_URL,
)

ROUTER = APIRouter()
ROUTER.include_router(health.router, prefix="/health", tags=["health"])
ROUTER.include_router(user.router, prefix="/user", tags=["user"])
ROUTER.include_router(auth.router, prefix="/auth", tags=["auth"])
ROUTER.include_router(article.router, prefix="/article", tags=["article"])


# Startup event
@APP.on_event("startup")
async def startup_event():
    logger.info("Processing startup initialization")


# Logs incoming request information
async def log_request(request: Request):
    logger.info(
        f"[{request.client.host}:{request.client.host}] {request.method} {request.url}"
    )
    logger.info(f"header: {request.headers}")


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
    ROUTER, prefix=settings.APP_PREFIX, dependencies=[Depends(log_request)]
)
