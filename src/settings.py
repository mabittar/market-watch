from enum import Enum
from functools import lru_cache
from os import environ
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(str, Enum):
    LOCAL = "local"
    PRODUCTION = "production"


class AppSettings(BaseSettings):
    TITLE: str = "Market Watch"
    VERSION: str = environ.get("APP_VERSION", "0.0.1")
    TIMEZONE: str = "UTC"
    DESCRIPTION: str = "Retrieve data from Market Sources"
    IS_DEBUG: bool = False
    DOCS_URL: str = environ.get("DOCS_URL", "/docs")
    OPENAPI_URL: str = environ.get("OPENAPI_URL", "/openapi.json")
    REDOC_URL: str = environ.get("REDOC_URL", "/redoc")
    OPENAPI_PREFIX: str = ""

    HOST: str = environ.get("SERVER_HOST", "localhost")
    PORT: int = int(environ.get("SERVER_PORT", 8000))
    WORKERS: int = int(environ.get("SERVER_WORKERS", 1))

    POLYGON_API_KEY: str = environ.get("POLYGON_API_KEY", "")
    POLYGON_API_TIMEOUT: int = int(environ.get("POLYGON_API_TIMEOUT", 500))

    model_config = SettingsConfigDict(
        env_file=f"{Path().resolve()}/.env",
        case_sensitive=True,
        validate_assignment=True,
        extra="allow",
    )

    @property
    def set_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.IS_DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
        }


class AppLocalSettings(AppSettings):
    ENVIRONMENT: AppEnvironment = AppEnvironment.LOCAL
    DESCRIPTION: str = f"Application ({ENVIRONMENT})."
    IS_DEBUG: bool = True


class AppProductionSettings(AppSettings):
    ENVIRONMENT: AppEnvironment = AppEnvironment.PRODUCTION
    DESCRIPTION: str = f"Application ({ENVIRONMENT})."


class FactoryAppSettings:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> AppSettings:
        if self.environment == AppEnvironment.PRODUCTION:
            return AppProductionSettings()
        return AppLocalSettings()


@lru_cache
def get_settings() -> AppSettings:
    return FactoryAppSettings(environment=environ.get("APP_ENV", "LOCAL"))()


settings = get_settings()
