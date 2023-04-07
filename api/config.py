import sys
from typing import Any, Dict, Optional

from dotenv import find_dotenv
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    class Config:
        env_file = find_dotenv(usecwd=True)
        env_file_encoding = "utf-8"

    """Application configuration"""
    APP_TITLE: str = "fastapi template"
    APP_DESCRIPTION: str = "A simple template for fastapi and complete workflow"
    APP_VERSION: str = "0.1.0"
    APP_OPENAPI_URL: str = "/openapi.json"
    APP_PREFIX: str = "/api"

    """Database configuration"""
    POSTGRES_DB: str = "fastapi-template"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "m3ow87"
    POSTGRES_PASSWORD: str = "m3ow87"
    POSTGRES_TEST_PORT: str = "5433"
    POSTGRES_DSN: Optional[PostgresDsn] = None

    @validator("POSTGRES_DSN", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Optional[PostgresDsn]:
        # if exists value and not empty
        if isinstance(v, str) and v != "":
            return v

        # choose which port should be used
        port = values.get("POSTGRES_PORT")
        if any("pytest" in arg for arg in sys.argv):
            port = values.get("POSTGRES_TEST_PORT")

        # choose which schema should be used, alembic use sync driver
        schema = "postgresql+asyncpg"
        if any("alembic" in arg for arg in sys.argv):
            schema = "postgresql"

        # build postgres dsn
        return PostgresDsn.build(
            scheme=schema,
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=port,
            path=f"/{values.get('POSTGRES_DB')}",
        )

    """ Core configuration """
    SECRET_KEY: str = "m3ow87"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ACCESS_TOKEN_ALGORITHM: str = "HS256"


settings = Settings()

# class Config:
#     APP_TITLE = _getenv("APP_TITLE", "fastapi template")
#     APP_DESCRIPTION = _getenv(
#         "APP_DESCRIPTION", "A simple template for fastapi and complete workflow"
#     )
#     APP_VERSION = _getenv("APP_VERSION", "0.1.0")
#     APP_OPENAPI_URL = _getenv("APP_OPENAPI_URL", "/openapi.json")
#     APP_PREFIX = _getenv("APP_PREFIX", "/api")

#     POSTGRES_DB = _getenv("POSTGRES_DB", "fastapi-template")
#     POSTGRES_HOST = _getenv("POSTGRES_HOST", "localhost")
#     POSTGRES_PORT = _getenv("POSTGRES_PORT", 5432)
#     POSTGRES_USER = _getenv("POSTGRES_USER", "m3ow87")
#     POSTGRES_PASSWORD = _getenv("POSTGRES_PASSWORD", "m3ow87")
#     POSTGRES_TEST_PORT = _getenv("POSTGRES_TEST_PORT", 5433)

#     @staticmethod
#     def get_db_url(driver: str = "postgresql") -> str:
#         # Decide which driver to use
#         driver_list = ["postgresql", "postgresql+asyncpg"]
#         if driver not in driver_list:
#             raise ValueError(f"Driver must be one of {driver_list}")

#         # Decide which port to use
#         port = settings.POSTGRES_PORT
#         if any("pytest" in arg for arg in sys.argv):
#             port = settings.POSTGRES_TEST_PORT

#         # Build url
#         url = (
#             f"{driver}://"
#             f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
#             f"{settings.POSTGRES_HOST}:{port}/"
#             f"{settings.POSTGRES_DB}"
#         )
#         return url

#     SECRET_KEY = _getenv("SECRET_KEY", "m3ow87")
#     # 60 minutes * 24 hours * 8 days = 8 days
#     ACCESS_TOKEN_EXPIRE_MINUTES = int(
#         _getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8)
#     )
#     ACCESS_TOKEN_ALGORITHM = _getenv("ACCESS_TOKEN_ALGORITHM", "HS256")
