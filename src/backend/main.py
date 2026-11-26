import logging
import pathlib
import time

from fastapi import FastAPI, Request

from backend.presentation.validation_handlers import register_validation_handlers
from backend.infrastructure.loggers.json_logger import setup_logging
from backend.infrastructure.loggers.helpers.request_context \
    import REQUEST_ID_HEADER, request_id_var, resolve_request_id

log_dir = pathlib.Path(__file__).resolve().parents[3] / "logs"
log_dir.mkdir(exist_ok=True)
setup_logging()


app = FastAPI()
register_validation_handlers(app)

@app.middleware("http")
async def request_context(request: Request, call_next):
    logger = logging.getLogger(__name__)
    request_id = resolve_request_id(request.headers.get(REQUEST_ID_HEADER))
    token = request_id_var.set(request_id)
    start = time.perf_counter()
    try:
        try:
          response = await call_next(request)
        except Exception:
          logger.exception(
            "unhandled exception",
            extra={
              "method": request.method,
              "path": request.url.path,
              "duration_ms": round((time.perf_counter() - start) * 1000, 1),
            },
          )
          raise
        response.headers[REQUEST_ID_HEADER] = request_id
        level = set_level(response.status_code)
        logger.log(
            level = level,
            msg = "request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - start) * 1000, 1),
            },
        )
        return response
    finally:
        request_id_var.reset(token)


def set_level(status_code: int) -> int:
  if status_code >= 500:
    return logging.ERROR
  elif status_code >= 400:
    return logging.WARNING
  else:
    return logging.INFO