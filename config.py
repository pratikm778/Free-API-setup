"""
Configuration settings for the Cascading AI API Flow
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Settings:
    """Global settings for the cascading API system"""

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "cascade_api.log"

    # Usage tracking
    USAGE_TRACKING_FILE: str = "usage_tracking.json"

    # Default API parameters
    DEFAULT_MAX_TOKENS: int = 500
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_RETRIES: int = 2

    # Backoff settings
    MAX_BACKOFF_DELAY: int = 60
    BASE_BACKOFF_DELAY: int = 2

    @classmethod
    def from_env(cls) -> 'Settings':
        """Create settings from environment variables"""
        return cls(
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
            LOG_FILE=os.getenv("LOG_FILE", "cascade_api.log"),
            USAGE_TRACKING_FILE=os.getenv("USAGE_TRACKING_FILE", "usage_tracking.json"),
            DEFAULT_MAX_TOKENS=int(os.getenv("DEFAULT_MAX_TOKENS", "500")),
            DEFAULT_TEMPERATURE=float(os.getenv("DEFAULT_TEMPERATURE", "0.7")),
            DEFAULT_MAX_RETRIES=int(os.getenv("DEFAULT_MAX_RETRIES", "2")),
        )

# Global settings instance
settings = Settings.from_env()
