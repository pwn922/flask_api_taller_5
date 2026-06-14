import logging
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class HTTPLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("http")
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(handler)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()
        self.logger.info(f"--> {request.method} {request.url.path}")

        response = await call_next(request)

        duration = time.perf_counter() - start_time
        self.logger.info(
            f"<-- {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {duration:.4f}s"
        )
        return response
