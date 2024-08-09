from fastapi import APIRouter, FastAPI

from src.presentation import router
from src.settings import AppSettings, settings


class App:
    def __init__(self, router: APIRouter, settings: AppSettings):
        self.__app = FastAPI(**settings.set_app_attributes)  # type: ignore
        self.__setup_middlewares(settings=settings)
        self.__add_routes(router=router, settings=settings)

    def __setup_middlewares(self, settings: AppSettings):
        pass

    def __add_routes(self, router: APIRouter, settings: AppSettings):
        self.__app.include_router(router=router)

    def __call__(self) -> FastAPI:
        return self.__app


def initialize_application() -> FastAPI:
    return App(router=router, settings=settings)()


app = initialize_application()

if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
