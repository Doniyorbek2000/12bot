import os
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Bot Configurations
    BOT_TOKEN: str
    ADMIN_IDS_RAW: str = "123456789"
    ADMIN_IDS: List[int] = []

    # Database Configurations
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/adolat_ai_bot"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Gemini AI Configurations
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # Payment Configurations
    PAYMENT_MODE: str = "mock"  # "mock", "live"
    CLICK_SERVICE_ID: str = ""
    CLICK_MERCHANT_ID: str = ""
    CLICK_SECRET_KEY: str = ""
    PAYME_MERCHANT_ID: str = ""
    PAYME_SECRET_KEY: str = ""

    # File Limits
    MAX_FREE_FILE_SIZE_MB: int = 1

    # App Settings
    APP_ENV: str = "development"  # "development", "production"
    WEBHOOK_URL: str = ""
    LOG_LEVEL: str = "INFO"

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v, info) -> List[int]:
        # Agar ADMIN_IDS to'g'ridan-to'g'ri berilgan bo'lsa yoki ADMIN_IDS_RAW orqali parse qilinsa
        raw_val = info.data.get("ADMIN_IDS_RAW", "123456789")
        if isinstance(raw_val, str):
            try:
                return [int(x.strip()) for x in raw_val.split(",") if x.strip()]
            except ValueError:
                return [123456789]
        return v if isinstance(v, list) else []

# Global settings instance
settings = Settings()
