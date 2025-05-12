
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    jwt_algorithm: str
    jwt_secret: str
    redis_host:str = "localhost"
    redis_port: int = 6379
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()