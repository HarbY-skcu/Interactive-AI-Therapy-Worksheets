import logging
import os
from logging.handlers import RotatingFileHandler

from pythonjsonlogger.json import JsonFormatter
from typing import List

from helpers.request_context import RequestIdFilter


def setup_logging(
  json_logs: bool = True,
  level: int = logging.INFO,
  log_file: str = None
) -> None:

    if json_logs:
      formatter = JsonFormatter(
        ["asctime", "levelname", "name", "request_id", "message"],
        rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
      )
    else:
      formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s [%(request_id)s]: %(message)s"
      )

    handlers = [logging.StreamHandler()]
    if log_file:
      os.makedirs(os.path.dirname(log_file), exist_ok=True)
      handlers.append(RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
      ))

    for handler in handlers:
      handler.addFilter(RequestIdFilter())
      handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers = handlers
    root.setLevel(level)