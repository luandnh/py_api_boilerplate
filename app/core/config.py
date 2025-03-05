import os
from enum import Enum

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class AppSettings(BaseSettings):
    APP_NAME: str = os.environ.get("APP_NAME", "API Example")
    APP_VERSION: str = os.environ.get("APP_VERSION", "1.0.0")
    APP_DESCRIPTION: str = os.environ.get("APP_DESCRIPTION", "API Example")


class DBSettings(BaseSettings):
    pass


class MySQLSettings(BaseSettings):
    MYSQL_USER: str = os.environ.get("MYSQL_USER", "username")
    MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD", "password")
    MYSQL_SERVER: str = os.environ.get("MYSQL_SERVER", "localhost")
    MYSQL_PORT: int = int(os.environ.get("MYSQL_PORT", "5432"))
    MYSQL_DB: str = os.environ.get("MYSQL_DB", "dbname")
    # Construct MYSQL_URI using the class variables
    MYSQL_URI: str = (
        f"{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    MYSQL_SYNC_PREFIX: str = os.environ.get("MYSQL_SYNC_PREFIX", "mysql+pymysql://")
    MYSQL_ASYNC_PREFIX: str = os.environ.get("MYSQL_ASYNC_PREFIX", "mysql+aiomysql://")
    MYSQL_URL: str = os.environ.get("MYSQL_URL", None)


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.environ.get("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.environ.get("REDIS_PASSWORD", None)
    REDIS_USERNAME: str = os.environ.get("REDIS_USERNAME", None)


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = EnvironmentOption(
        os.environ.get("ENVIRONMENT", "local")
    )


class Settings(
    AppSettings, DBSettings, MySQLSettings, RedisSettings, EnvironmentSettings
):
    pass


settings = Settings()
