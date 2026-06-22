from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "AprovAI API"
    API_V1_STR: str = "/api/v1"
    
    # Database config (defaults to SQLite if POSTGRES_URL is not set)
    DATABASE_URL: str = Field(default="sqlite:///./sqlite.db")
    
    # Gemini AI configuration
    GEMINI_API_KEY: str = Field(default="mock_api_key")
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash"

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:4200", "http://127.0.0.1:4200"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
