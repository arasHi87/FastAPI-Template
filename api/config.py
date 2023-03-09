import os
import sys

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
        "APP_DESCRIPTION", "A simple template for fastapi and complete workflow"
    )
    APP_VERSION = _getenv("APP_VERSION", "0.1.0")
    APP_OPENAPI_URL = _getenv("APP_OPENAPI_URL", "/openapi.json")
    APP_PREFIX = _getenv("APP_PREFIX", "/api")

    POSTGRES_DB = _getenv("POSTGRES_DB", "fastapi-template")
    POSTGRES_HOST = _getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = _getenv("POSTGRES_PORT", 5432)
    POSTGRES_USER = _getenv("POSTGRES_USER", "m3ow87")
    POSTGRES_PASSWORD = _getenv("POSTGRES_PASSWORD", "m3ow87")
    POSTGRES_TEST_PORT = _getenv("POSTGRES_TEST_PORT", 5433)

    @staticmethod
    def get_db_url(driver: str = "postgresql") -> str:
        # Decide which driver to use
        driver_list = ["postgresql", "postgresql+asyncpg"]
        if driver not in driver_list:
            raise ValueError(f"Driver must be one of {driver_list}")

        # Decide which port to use
        port = Config.POSTGRES_PORT
        if any("pytest" in arg for arg in sys.argv):
            port = Config.POSTGRES_TEST_PORT

        # Build url
        url = (
            f"{driver}://"
            f"{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@"
            f"{Config.POSTGRES_HOST}:{port}/"
            f"{Config.POSTGRES_DB}"
        )
        return url

    PASSWORD_SALT = _getenv("PASSWORD_SALT", "m3ow87")
