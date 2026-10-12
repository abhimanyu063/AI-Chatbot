
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Retail Competitive Intelligence API"
    DEBUG: bool = True

    FRONTEND_URL: str = "http://localhost:5173"

    # SQL Planner integration
    USE_MOCK_SQL: bool = True
    SQL_PLANNER_URL: str = ""
    SQL_PLANNER_API_KEY: str = ""
    SQL_PLANNER_TIMEOUT: float = 20.0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
