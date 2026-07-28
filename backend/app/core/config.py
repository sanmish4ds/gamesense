import re
from pydantic_settings import BaseSettings
from pydantic import model_validator


class Settings(BaseSettings):
    # Accepts postgres://, postgresql://, or postgresql+asyncpg://
    DATABASE_URL: str = "postgresql+asyncpg://gamesense:gamesense@localhost:5432/gamesense"
    SYNC_DATABASE_URL: str = ""  # derived automatically when blank
    REDIS_URL: str = "redis://localhost:6379/0"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_SECURITY_PROTOCOL: str = "PLAINTEXT"
    KAFKA_SASL_MECHANISM: str = "PLAIN"
    KAFKA_SASL_USERNAME: str = ""
    KAFKA_SASL_PASSWORD: str = ""
    CRICAPI_KEY: str = ""
    SECRET_KEY: str = "dev-secret"
    ENVIRONMENT: str = "development"
    POLL_INTERVAL_SECONDS: int = 10

    @model_validator(mode="after")
    def _normalize_db_urls(self) -> "Settings":
        url = self.DATABASE_URL
        # Render supplies postgres:// — normalize to postgresql://
        url = re.sub(r"^postgres://", "postgresql://", url)
        if "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.DATABASE_URL = url
        if not self.SYNC_DATABASE_URL:
            self.SYNC_DATABASE_URL = url.replace("+asyncpg", "")
        return self

    class Config:
        env_file = ".env"


settings = Settings()
