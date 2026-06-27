from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://gamesense:gamesense@localhost:5432/gamesense"
    SYNC_DATABASE_URL: str = "postgresql://gamesense:gamesense@localhost:5432/gamesense"
    REDIS_URL: str = "redis://localhost:6379/0"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    CRICAPI_KEY: str = ""
    SECRET_KEY: str = "dev-secret"
    ENVIRONMENT: str = "development"
    POLL_INTERVAL_SECONDS: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
