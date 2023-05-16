from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

PROJECT_ROOT: Path = Path(__file__).parent.resolve()
APP_NAME = "event_board"

FILE_LOG_SIZE = 32 * 1024**2  # 32 MiB
FILE_LOG_COUNT = 5
# these are placed in Settings.logs_directory
DISCORD_LOG_FILE_NAME = "discord.log"
APP_LOG_FILE_NAME = "app.log"


class Settings(BaseSettings):
    discord_auth_token: str
    guild_id: int
    logs_directory: Path = PROJECT_ROOT / "logs"
    # TODO add typehints (enums or literals) to log levels
    # TODO replace log level defaults with non DEBUG ones (maybe WARN or ERRORS only? - i thin app can stay as info)
    discord_log_level: str = "INFO"
    app_log_level: str = "DEBUG"
    html_output_path: Path = PROJECT_ROOT / "output.html"
    html_locale: str = "en_UK"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
