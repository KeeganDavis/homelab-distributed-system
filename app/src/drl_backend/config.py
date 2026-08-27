import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str
    log_level: str


settings = Settings(
    app_env=os.getenv("APP_ENV", "development"),
    log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
)