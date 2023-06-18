from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = 'dev'

    DATABASE_URL: str = 'postgresql+asyncpg://postgres:change-me@postgres:5432/postgres'


settings = Settings()
