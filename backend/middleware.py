import datetime

from logging import getLogger, StreamHandler, INFO

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(INFO)

class AccessLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        start_time = datetime.datetime.now()
        response = await call_next(request)
        end_time = datetime.datetime.now()

        response_time = (end_time - start_time).total_seconds() * 1000
        client_ip = request.headers.get("x-forwarded-for", "-")
        method = request.method
        path = request.url.path + ("?" + request.url.query if request.url.query else "")
        status = response.status_code
        content_length = response.headers.get("content-length", "-")
        referer = request.headers.get("referer", "-")
        user_agent = request.headers.get("user-agent", "-")

        # Log
        logger.info(f"{client_ip} - - [{start_time}] \"{method} {path} HTTP/1.1\" {status} {content_length} \"{referer}\" \"{user_agent}\" {response_time:.0f}")

        return response

