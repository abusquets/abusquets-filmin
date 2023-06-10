from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = 'dev'


settings = Settings()
