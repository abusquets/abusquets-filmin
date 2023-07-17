from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Filmin API'
    PROJECT_DESCRIPTION: str = 'Filmin API - PROOF OF CONCEPT'
    VERSION: str = '0.1.0'
    APP_LOGGER_NAME: str = 'filmin_poc'

    APP_ENV: str = 'dev'
    DEBUG: bool = False

    DATABASE_URL: str = 'postgresql+asyncpg://postgres:change-me@postgres:5432/postgres'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    JWT_ALGORITHM: str = 'HS256'
    JWT_SECRET_KEY: str = 'change-me'
    JWT_REFRESH_SECRET_KEY: str = 'change-me'

    REDIS_URL: str = 'redis://redis:6379/0'
    REDIS_USER: str = 'default'
    REDIS_PASSWORD: str = 'change-me'


settings = Settings()
