import abc
import json

from fastapi import Request, Response
from starlette.types import ASGIApp
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..settings import settings
from ..infra.logger import log


class BaseHttpMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.logger = log
        self.env_settings = settings

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            await self.process_request(request)
            response: Response = await call_next(request)
            await self.process_response(request, response)
        except StarletteHTTPException as exc:
            request_body = await request.body()
            self.default_error_logger(
                **{
                    "request_body": request_body.decode("utf-8"),
                    "request_headers": dict(request.headers),
                    "request_query_params": dict(request.query_params),
                    "request_method": request.method,
                    "request_url": str(request.url),
                    "error_message": str(exc),
                },
            )
            raise exc

        return response

    @abc.abstractmethod
    async def process_request(self, request: Request):
        pass

    @abc.abstractmethod
    async def process_response(self, request: Request, response: Response):
        pass

    @staticmethod
    def request_path(request: Request) -> str:
        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"
        return path

    def default_error_logger(self, **kwargs):
        self.logger.err(json.dumps(kwargs, indent=4))

    def default_info_logger(self, **kwargs):
        self.logger.info(json.dumps(kwargs, indent=4))
