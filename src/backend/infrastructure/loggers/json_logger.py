import atexit
import json
import logging
import pathlib


def setup_logging() -> None:
  config_file_location = pathlib.Path(__file__).parent / "root_logging_config.json"
  with open(config_file_location) as config_file:
    config_contents = json.load(config_file)
  logging.config.dictConfig(config_contents)

  queue_handler = logging.getHandlerByName("queue_handler")
  if queue_handler is not None:
    queue_handler.listener.start()
    atexit.register(queue_handler.listener.stop)