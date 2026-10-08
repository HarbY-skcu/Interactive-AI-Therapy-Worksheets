import logging
import time

from fastapi import FastAPI, Request

from src.backend.infrastructure.loggers.json_logger import setup_logging
from src.backend.infrastructure.loggers.helpers.request_context \
    import REQUEST_ID_HEADER, request_id_var, resolve_request_id


setup_logging(json_logs=True)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = resolve_request_id(request.headers.get(REQUEST_ID_HEADER))
    token = request_id_var.set(request_id)
    start = time.perf_counter()
    try:
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        logger.info(
            "request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - start) * 1000, 1),
            },
        )
        return response
    except Exception:
        logger.exception(
            "unhandled exception",
            extra = {
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round((time.perf_counter() - start) * 1000, 1),
            },
        )
        raise
    finally:
        request_id_var.reset(token)