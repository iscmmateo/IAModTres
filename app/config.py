from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    JWT_SECRET: str = Field("change-me", description="JWT signing secret")
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    RATE_LIMIT_GENERAL: str = "100/minute"
    RATE_LIMIT_LOGIN: str = "5/minute"

    class Config:
        env_file = ".env"

settings = Settings()
