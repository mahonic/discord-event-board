import logging.handlers
from pathlib import Path

from config import (
    APP_LOG_FILE_NAME,
    APP_NAME,
    DISCORD_LOG_FILE_NAME,
    FILE_LOG_COUNT,
    FILE_LOG_SIZE,
    get_settings,
)

settings = get_settings()
dt_fmt = "%Y-%m-%d %H:%M:%S"
default_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)

# create the log directory if it doesn't exist
settings.logs_directory.mkdir(parents=True, exist_ok=True)


def create_a_logger(
    *,
    loger_name: str,
    log_level: str,
    rotating_log_file_name: Path | str | None = None,
    output_to_stderr: bool = True,
    formatter: logging.Formatter = default_formatter,
):
    logger = logging.getLogger(loger_name)
    logger.setLevel(log_level)
    if rotating_log_file_name:
        file_log_handler = logging.handlers.RotatingFileHandler(
            filename=rotating_log_file_name,
            encoding="utf-8",
            maxBytes=FILE_LOG_SIZE,
            backupCount=FILE_LOG_COUNT,
        )
        file_log_handler.setFormatter(formatter)
        logger.addHandler(file_log_handler)
    if output_to_stderr:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger


discord_logger = create_a_logger(
    loger_name="discord",  # TODO make a variable, even in this file, like DISCORD_LOGGER_NAME="discord"
    log_level=settings.discord_log_level,
    rotating_log_file_name=settings.logs_directory / DISCORD_LOG_FILE_NAME,
    output_to_stderr=True,
)

app_logger = create_a_logger(
    loger_name=APP_NAME,
    log_level=settings.app_log_level,
    rotating_log_file_name=settings.logs_directory / APP_LOG_FILE_NAME,
    output_to_stderr=True,
)
