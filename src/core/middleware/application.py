import re
import time
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from context import correlation_id_ctx
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


logger = logging.getLogger("access")


class ApplicationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        header_process_id_name: str = "X-Api-Request-ID",
        header_process_time_name: str = "X-Api-Process-Time",
    ):
        super().__init__(app)
        self.header_request_id_name = header_process_id_name
        self.header_process_time_name = header_process_time_name

    async def dispatch(self, request: Request, call_next):
        request_id: str = str(uuid4())
        start_time = time.perf_counter_ns()
        correlation_id_ctx.set(request_id)
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(e)
            msg = "Exception Occurred!"
            response = JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "type": type(msg).__name__,
                        "detail": msg,
                    }
                },
            )

        end_time = time.perf_counter_ns()
        elapsed_time_ns = end_time - start_time
        elapsed_time_ms = elapsed_time_ns / 1000000
        response.headers[self.header_request_id_name] = request_id
        response.headers[self.header_process_time_name] = f"{elapsed_time_ms:.2f} ms"
        logger.info(f'"{request.method} {request.url}" {response.status_code} {elapsed_time_ms:.2f} ms')
        return response
