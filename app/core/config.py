"""
Configuration settings for the Energetic Backend
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Energetic Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # CORS
    ALLOWED_HOSTS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080", "http://localhost:8000"],
        env="ALLOWED_HOSTS"
    )
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:password@localhost:5432/energetic_db",
        env="DATABASE_URL"
    )
    
    # Anthropic API
    ANTHROPIC_API_KEY: str = Field(..., env="ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = Field(
        default="claude-sonnet-4-20250514",
        env="ANTHROPIC_MODEL"
    )
    
    # Computer Use Agent
    COMPUTER_USE_TOOL_VERSION: str = Field(
        default="computer_use_20250124",
        env="COMPUTER_USE_TOOL_VERSION"
    )
    MAX_OUTPUT_TOKENS: int = Field(default=128000, env="MAX_OUTPUT_TOKENS")
    
    # VNC Settings
    VNC_HOST: str = Field(default="localhost", env="VNC_HOST")
    VNC_PORT: int = Field(default=5900, env="VNC_PORT")
    VNC_PASSWORD: str = Field(default="", env="VNC_PASSWORD")
    
    # Session Management
    SESSION_TIMEOUT_MINUTES: int = Field(default=60, env="SESSION_TIMEOUT_MINUTES")
    MAX_SESSIONS_PER_USER: int = Field(default=5, env="MAX_SESSIONS_PER_USER")
    
    # Streaming
    STREAMING_CHUNK_SIZE: int = Field(default=1024, env="STREAMING_CHUNK_SIZE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


# Global settings instance
settings = Settings()
