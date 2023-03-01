import os

from dotenv import load_dotenv

load_dotenv()


def _getenv(key: str, default: str = None) -> str:
    value = os.environ.get(key, default)
    if value is None:
        raise NameError(f'Environment key "{key}" not found, recheck your .env file.')
    return value


class Config:
    APP_TITLE = _getenv("APP_TITLE", "fastapi template")
    APP_DESCRIPTION = _getenv(
        "APP_DESCRIPTION", "A simple templae for fastapi and complete workflow"
    )
    APP_VERSION = _getenv("APP_VERSION", "0.1.0")
    APP_OPENAPI_URL = _getenv("APP_OPENAPI_URL", "/openapi.json")
    APP_PREFIX = _getenv("APP_PREFIX", "/api")
