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

    POSTGRES_DB = _getenv("POSTGRES_DB", "fastapi-template")
    POSTGRES_HOST = _getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = _getenv("POSTGRES_PORT", 5432)
    POSTGRES_USER = _getenv("POSTGRES_USER", "m3ow87")
    POSTGRES_PASSWORD = _getenv("POSTGRES_PASSWORD", "m3ow87")
    BASE_DB_URL = f"://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    @staticmethod
    def get_db_url(driver: str = "postgresql") -> str:
        driver_list = ["postgresql", "postgresql+asyncpg"]
        if driver not in driver_list:
            raise ValueError(f"Driver must be one of {driver_list}")
        return f"{driver}{Config.BASE_DB_URL}"

    PASSWORD_SALT = _getenv("PASSWORD_SALT", "m3ow87")
