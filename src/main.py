from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any, List

from fastapi import APIRouter, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .infra.db.session import sessionmanager
from .infra.logger import log
from .middlewares import middlewares
from .presentation import router
from .settings import AppSettings, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    log.info(msg="Welcome 🛬")
    log.info(msg=f"Application v{app.version} started elegantly!")
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()
    log.info(msg="Goodbye 🚀")
    log.info(msg=f"Application v{app.version} shut down gracefully!")


class App:

    def __init__(
        self,
        lifespan: Callable,
        router: APIRouter,
        settings: AppSettings,
        middlewares: List[BaseHTTPMiddleware],
    ):
        self.__app = FastAPI(lifespan=lifespan, **settings.set_app_attributes)  # type: ignore
        self.__setup_middlewares(middlewares=middlewares, settings=settings)
        self.__add_routes(router=router, settings=settings)

    def __setup_middlewares(
        self,
        middlewares: List[BaseHTTPMiddleware],
        settings: AppSettings,
    ):
        if middlewares:
            for middleware in middlewares:
                self.__app.add_middleware(middleware) # type: ignore

    def __add_routes(self, router: APIRouter, settings: AppSettings):
        self.__app.include_router(router=router)

    def __call__(self) -> FastAPI:
        return self.__app


def initialize_application() -> FastAPI:
    return App(
        lifespan=lifespan, router=router, settings=settings, middlewares=middlewares # type: ignore
    )()


app = initialize_application()
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
