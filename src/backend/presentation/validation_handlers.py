from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

INVALID_EMAIL_DETAIL = "Invalid Email Address, Try Again"
INVALID_CREDENTIALS_DETAIL = "Incorrect Credentials, try again"


def _detail_for(exc: RequestValidationError) -> str:
  """Pick a client-safe message without echoing any submitted input."""
  messages = " ".join(str(error.get("msg", "")) for error in exc.errors())
  if "Invalid email address" in messages:
    return INVALID_EMAIL_DETAIL
  return INVALID_CREDENTIALS_DETAIL


async def validation_error_handler(
  request: Request,
  exc: RequestValidationError,
) -> JSONResponse:
  return JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content={"detail": _detail_for(exc)},
  )


def register_validation_handlers(app: FastAPI) -> None:
  app.add_exception_handler(RequestValidationError, validation_error_handler)
