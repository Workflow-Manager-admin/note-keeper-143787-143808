import os
from typing import Optional

# Handle different pydantic versions
try:
    from pydantic_settings import BaseSettings
except ImportError:
    try:
        from pydantic import BaseSettings
    except ImportError:
        # Fallback for basic configuration
        class BaseSettings:
            def __init__(self):
                pass


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    app_name: str = "Notes API"
    app_version: str = "1.0.0"
    app_description: str = "A REST API for managing notes with full CRUD operations"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Database Settings
    data_file: Optional[str] = None  # Path to JSON file for data persistence
    
    # CORS Settings
    cors_origins: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

# Initialize database with data file if specified
if settings.data_file:
    # Ensure the directory exists
    data_dir = os.path.dirname(settings.data_file)
    if data_dir:
        os.makedirs(data_dir, exist_ok=True)
