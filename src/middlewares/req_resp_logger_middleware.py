import time

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from .base_middleware import BaseHttpMiddleware


class ReqRespLoggerMiddleware(BaseHttpMiddleware):
    async def process_request(self, request: Request) -> Request:
        request.state.start_time = time.perf_counter()
        path = self.request_path(request)
        incoming_msg = {
            "msg": f"INCOMING REQUEST: {request.method.upper()} {path}",
            "method": request.method.upper(),
            "endpoint": path,
            "ip_address": request.client.host,  # type: ignore
        }
        self.default_info_logger(**incoming_msg)
        return request

    async def process_response(self, request: Request, response: Response) -> Response:
        path = self.request_path(request)
        process_time = round((time.perf_counter() - request.state.start_time) * 1000, 2)
        if isinstance(response, JSONResponse) and response.headers is not None:
            response.headers["Process Time"] = str(process_time)

        status_code = getattr(response, "status_code", None)

        outgoing_msg = {
            "msg": f"OUTGOING RESPONSE: {request.method.upper()} {path} status_code: {status_code} took {process_time} ms",
            "method": request.method.upper(),
            "endpoint": path,
            "status": status_code,
            "took": int(round(process_time, 0)),
            "ip_address": request.client.host,  # type: ignore
        }
        self.default_info_logger(**outgoing_msg)

        return response
