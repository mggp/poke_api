from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    poke_api_path: str
    float_decimal_places: int = 0
    logger_level: str = "INFO"


class RedisSettings(BaseSettings):
    db: int = 0
    host: str = "localhost"
    port: int = 6379
    password: str = ""
    enabled: bool = False
    default_expiration: int = 3600

    model_config = SettingsConfigDict(env_prefix="REDIS_")


settings = Settings()
redis_settings = RedisSettings()
