import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from ..loggers.execution_time_logger import execution_time_logger
from uuid import uuid4

class ExecutionTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            request_id = str(uuid4())
            response = await call_next(request)
        except Exception as e:
            execution_time_logger.error(f"Request failed: {e}")
            raise e
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            execution_time_logger.info(  
                msg="Request and execution time details",
                extra={
                    "execution_time": execution_time,
                    "request_id": request_id,
                    "endpoint": request.url.path,
                    "method": request.method

                })
        return response
