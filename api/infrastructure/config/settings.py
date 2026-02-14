"""Configuration settings for the MangoAI Agent."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI API
    openai_api_key: str = ""

    # Mango Reach API (the main backend)
    mango_reach_api_url: str = "http://localhost:8008"

    # Security
    secret_key: str = ""
    algorithm: str = "HS256"

    # Agent
    app_name: str = "mango_ai"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow extra fields in .env


settings = Settings()
