import logging
import os

from collector_src.config.settings import settings

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    level = getattr(logging, settings.logging_level)

    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    os.makedirs("logs", exist_ok=True)

    file_handler = logging.FileHandler(settings.log_file)
    file_handler.setFormatter(formatter)

    return logger